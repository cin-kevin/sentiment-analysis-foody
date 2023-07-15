
import scrapy
from scrapy_splash import SplashRequest 
from scrapy import Request
import json, re
from crawl.items import FoodyItem, FoodyCommentItem
from crawl.config import cfg

lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(2))

    splash:set_viewport_full()
    
    assert(splash:runjs("document.getElementsByName('Email')[0].value = '{0}'"))
    assert(splash:runjs("document.getElementsByName('Password')[0].value = '{1}'"))
     
    local password_submit = splash:select('input[id=bt_submit]')
    password_submit:mouse_click()
    assert(splash:wait(2))
    
    local png = splash:png()

    return {
        html=splash:html(),
        url = splash:url(),
        cookies = splash:get_cookies(),
        png = png,
        }
    end
"""
lua_script = lua_script.replace("{0}", cfg.username).replace("{1}", cfg.password)


class FoodyLoginSpider(scrapy.Spider):
    name = "foody"
    start_urls = [
        'http://www.foody.vn/ho-chi-minh/quan-an',
        'http://www.foody.vn/ho-chi-minh/an-vat-via-he',
        'http://www.foody.vn/ho-chi-minh/tiem-banh',
        'http://www.foody.vn/ho-chi-minh/nha-hang',
        'http://www.foody.vn/ho-chi-minh/an-chay'
    ]
    allowed_domains = ["www.foody.vn"]
    provider_per_page = 12
    comment_per_page = 10
    provinceId = 217  # Saigon
    magic_number = 20 # don't ask why, it's magic ^.^
    category = {
        'quan-an': 3,
        'an-vat-via-he': 11,
        'tiem-banh': 6,
        'nha-hang': 1,
        'an-chay': 56
    }
    
    header_template = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'en-US,vi;q=0.5',
                   'Referer': '',
                   'DNT': 1,
                   'Host': 'www.foody.vn',
                   'Pragma': 'no-cache',
                   'X-Foody-User-Token': '49f6ad1b-e2dc-4b68-ad0d-b18f64cb146c',
                   'X-Requested-With': 'XMLHttpRequest'}

    def start_requests(self):
        signin_url = 'https://id.foody.vn/account/login?returnUrl=https://www.foody.vn/'
        yield SplashRequest(
            url=signin_url, 
            callback=self.start_scrapping,
            endpoint='execute', 
            args={
                'width': 1000,
                'lua_source': lua_script,
                'ua': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                'png': 1,
                },
            )
    
    def start_scrapping(self,response):
        url = "https://www.foody.vn"
        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=cookies_dict, callback=self.parse_restaurant)

    def parse_restaurant(self, response):
        """
        First step: yield request
        """
        page_name_ = re.sub('https://www.foody.vn/ho-chi-minh/', '', response.url)
        category_id = self.category[page_name_]
        total_ = response.xpath("//div[@class='result-status-count']/div/span/text()").extract()[0]
        total_page_ = int(int(re.sub('\.', '', total_)) / self.provider_per_page)
        header_ = self.header_template
        header_['Referer'] = response.url
        priority_ = self.magic_number
        for sub_page in range(1, total_page_):
            url_ = 'http://www.foody.vn/ho-chi-minh/dia-diem?ds=Restaurant&vt=row&st=1&dt=undefined&c=3&' \
                   'page={}&provinceId={}&categoryId={}&append=true'.format(sub_page, self.provinceId, category_id)
            yield Request(url=url_, dont_filter=True, meta={'page': sub_page}, callback=self.parse_restaurant_detail,
                          headers=header_,priority=priority_)
            priority_ -= 1
            
    def parse_restaurant_detail(self, response):
        """
        Second step: yield item
        Response Url Sample: https://www.foody.vn/ho-chi-minh/quan-an
        """
        header_ = self.header_template
        header_['Referer'] = response.url
        priority_ = self.magic_number
        response_ = json.loads(response.body)
        for i in response_['searchItems']:
            item = FoodyItem()
            item['main_url'] = self.allowed_domains[0] + i['DetailUrl']
            item['addr'] = i['Address']
            item['rating'] = i['AvgRating']
            item['id'] = i['Id']
            item['totalreview'] = i['TotalReview']
            item['name'] = i['Name']
            
            yield Request(url=f"https://{item['main_url']}",
                          dont_filter=True, 
                          meta={'restaurant': item},
                          callback=self.parse_first_comment,
                          headers=header_,
                          priority=priority_)
            
            yield item

    def parse_first_comment(self, response):
        """
        Third step: get comment list
        Response Url Sample: https://www.foody.vn/ho-chi-minh/heart-kitchen-bo-ne-hau-ne
        """
        header_ = self.header_template
        header_['Referer'] = response.url
        priority_ = self.magic_number
        restaurant = response.meta['restaurant']
        resid = restaurant['id']
        # https://www.foody.vn/__get/Review/ResLoadMore?t=1689170724828&ResId=373&LastId=6872006&Count=5&Type=1&fromOwner=&isLatest=true&ExcludeIds=
        url_ = 'https://www.foody.vn/__get/Review/ResLoadMore?t=undefined&' \
                'ResId={}&LastId=undefined&Count={}&Type=1&isLatest=true'.format(resid, 5)
        yield Request(
            url=url_,
            dont_filter=True,
            meta={
                'referer_url': response.url,
                'restaurant': restaurant},
            callback=self.parse_comment_detail,
            headers=header_, priority=priority_)

    def parse_comment_detail(self, response):
        """
        Last step: get comment list recursively
        Response Url Sample: https://www.foody.vn/ho-chi-minh/heart-kitchen-bo-ne-hau-ne
        """
        priority_ = self.magic_number
        
        header_ = self.header_template
        header_['Referer'] = response.meta['referer_url']
        
        restaurant = response.meta['restaurant']
        resid = restaurant['id']
        
        response_ = json.loads(response.body)
        lastid = response_['LastId']
        comments = response_['Items']
        # https://www.foody.vn/__get/Review/ResLoadMore?t=1689170724828&ResId=373&LastId=6872006&Count=5&Type=1&fromOwner=&isLatest=true&ExcludeIds=
        
        if len(comments) > 0:
            url_ = 'https://www.foody.vn/__get/Review/ResLoadMore?t=undefined&' \
                    'ResId={}&LastId={}&Count={}&Type=1&isLatest=true'.format(resid, lastid, 5)
            yield Request(
                url=url_,
                dont_filter=True,
                meta={
                    'referer_url': response.meta['referer_url'],
                    'restaurant': restaurant},
                callback=self.parse_comment_detail,
                headers=header_, priority=priority_)
            
            for comment in comments:
                item = FoodyCommentItem()
                item['id'] = comment['Id']
                item['description'] = comment['Description']
                item['rating'] = comment['AvgRating']
                item['url'] = comment['Url']
                item['resid'] = resid
                yield item

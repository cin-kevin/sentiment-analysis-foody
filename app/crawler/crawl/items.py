# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodyItem(scrapy.Item):
    main_url = scrapy.Field() # DetailUrl
    addr = scrapy.Field() # Address
    rating = scrapy.Field() # AvgRating
    id = scrapy.Field() # Id
    totalreview = scrapy.Field() #TotalReview
    name = scrapy.Field() # Name
    pass


class FoodyCommentItem(scrapy.Item):
    rating = scrapy.Field() # AvgRating
    description = scrapy.Field() # Description
    id = scrapy.Field() # Id
    url = scrapy.Field() # Url
    resid = scrapy.Field()
    pass


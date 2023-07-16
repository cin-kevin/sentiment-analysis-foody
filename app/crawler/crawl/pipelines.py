# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys
from pathlib import Path

path_s = Path(__file__).parent.parent.parent
sys.path.append(str(path_s))

from shared.db.repo import BaseRepo
from shared.db.schemas import Comment, Restaurant

from .items import FoodyCommentItem, FoodyItem

repo = BaseRepo()


class CrawlPipeline:
    def process_item(self, item, spider):
        if type(item).__name__ == FoodyItem.__name__:
            self.insert_restaurant(item)
        elif type(item).__name__ == FoodyCommentItem.__name__:
            self.insert_comments(item)
        return item

    def insert_restaurant(self, restaurant: FoodyItem):
        res = Restaurant()
        res.id = restaurant["id"]
        res.name = restaurant["name"]
        res.address = restaurant["addr"]
        res.url = restaurant["main_url"]
        repo.insert_restaurant(res)

    def insert_comments(self, comment: FoodyCommentItem):
        cmt = Comment()
        cmt.id = comment["id"]
        cmt.content = comment["description"]
        cmt.url = comment["url"]
        cmt.rating = comment["rating"]
        cmt.restaurant_id = comment["resid"]
        repo.insert_comment(cmt)

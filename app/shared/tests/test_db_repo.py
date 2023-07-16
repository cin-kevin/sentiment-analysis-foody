import unittest
from shared.db.repo import BaseRepo
from shared.db.schemas import Base, Restaurant, Comment
from shared.db.models import CommentUpdate
from sqlalchemy import create_engine
from initdb import init


class TestBaseRepo(unittest.TestCase):
    engine = create_engine('sqlite:///:memory:')
    repo = BaseRepo(engine_in=engine)
    
    def setUp(self):
        Base.metadata.create_all(self.engine)
        init(engine_in=self.engine)
        
    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_get_user(self):
        user = self.repo.get_user("CTV", "1")
        self.assertTrue(user is not None)
        
    def test_insert_restaurant(self):
        restaurant = Restaurant()
        restaurant.id = 100
        restaurant.address = "Test address"
        restaurant.name = "Hadilao"
        restaurant.url = "http://www.foody.vn/hadilao"
        
        res = self.repo.insert_restaurant(restaurant)
        
        self.assertTrue(res is not None)
        
    def test_insert_comment(self):
        comment = Comment()
        comment.id = 100
        comment.restaurant_id = 1
        comment.content = "Test"
        comment.need_review = False
        
        cmt = self.repo.insert_comment(comment)
        
        self.assertTrue(cmt is not None)
        self.assertTrue(cmt.content == "Test")
        
    def test_update_comment(self):
        comment_in = CommentUpdate()
        comment_in.id = 1
        comment_in.verified_result = "NEG"
        comment_in.restaurant_id = 1
        
        cmt = self.repo.update_comment(comment_in)
        self.assertTrue(cmt is not None)
        self.assertTrue(cmt.verified_result == "NEG")
        
    def test_get_comment(self):
        cmt = self.repo.get_comment(1)
        self.assertTrue(cmt.id == 1)
        
    def test_get_comments_to_predict(self):
        cmts = self.repo.get_comments_to_predict(0, 10)
        
        self.assertTrue(len(cmts), 3)
        
        
    def test_get_comments_mismatch_prediction(self):
        cmts = self.repo.get_comments_mismatch_prediction(0, 10)
        
        self.assertTrue(len(cmts), 3)

if __name__ == '__main__':
    unittest.main()
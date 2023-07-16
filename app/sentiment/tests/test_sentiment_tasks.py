import unittest
from unittest.mock import patch, Mock
from ..tasks import (
    _parse_limit_token, 
    _predict, 
    _update_comment_result)
from shared.db.repo import BaseRepo
from lorem_text import lorem

class TestSentimentTask(unittest.TestCase):
    repo_mock: BaseRepo = Mock()
    
    def test_parse_limit_token(self):
        input = lorem.words(200)
        content = _parse_limit_token(input)
        self.assertTrue(len(content.split()) == 100)

    def test_predict(self):
        pred = _predict("Trải nghiệm không tốt")
        self.assertTrue(pred == "NEG")

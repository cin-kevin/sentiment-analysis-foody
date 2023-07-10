import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from .celery import app
from shared.db.repo import BaseRepo
from shared.db.schemas import Comment
from shared.db.models import CommentUpdate
import logging


logger = logging.getLogger(__name__)
repo = BaseRepo()

@app.task(autoretry_for=(Exception,), retry_backoff=True)
def sentiment_analyze_task(commentid):
    """
     Task to analyze sentiment. This task is used in conjunction with
     func : ` RobertaForSequenceClassification. analyze_sentence `
     
     @param sentence - The sentence to analyze
    """
    comment: Comment = repo.get_comment(commentid)

    if comment:
        pred_result = _predict(comment.content)
        logger.info(f"prediction result is {pred_result}")
        _update_comment_result(pred_result, comment)
        logger.info("updated to database")


def _predict(content):
    label = ["NEG", "POS", "NEU"]

    model = RobertaForSequenceClassification.from_pretrained("./sentiment/phobert-base-vietnamese-sentiment") # noqa

    tokenizer = AutoTokenizer.from_pretrained("./sentiment/phobert-base-vietnamese-sentiment", use_fast=False) # noqa

    input_ids = torch.tensor([tokenizer.encode(content)])

    with torch.no_grad():
        out = model(input_ids)
        output = out.logits.softmax(dim=-1).tolist()[0]
        return label[output.index(max(output))]


def _update_comment_result(pred_result: str, comment: Comment):
    comment_in: CommentUpdate = CommentUpdate.from_orm(comment)
    
    comment_in.model_prediction = pred_result

    comparing_rating = "NEG"

    if comment_in.rating >= 7:
        comparing_rating = "POS"
    elif comment_in.rating >= 5 and comment_in.rating < 7:
        comparing_rating = "NEU"

    comment_in.need_review = not (comparing_rating == pred_result)
    logger.info(f"comment need review is {comment_in.need_review}")
    
    repo.update_comment(comment_in)

import logging

import torch
from shared.db.models import CommentUpdate
from shared.db.repo import BaseRepo
from shared.db.schemas import Comment
from transformers import AutoTokenizer, RobertaForSequenceClassification

from .celery import app

logger = logging.getLogger(__name__)
repo = BaseRepo(None)


@app.task(autoretry_for=(Exception,), retry_backoff=True)
def sentiment_analyze_task():
    """
    Task to analyze sentiment. This task is used in conjunction with
    func : ` RobertaForSequenceClassification. analyze_sentence `

    @param sentence - The sentence to analyze
    """
    comments: list[Comment] = repo.get_comments_to_predict(0, 50)
    logger.info(f"Found {len(comments)} comments not analyzed")

    for comment in comments:
        if comment:
            try:
                content = _parse_limit_token(comment.content)
                pred_result = _predict(content)
                logger.info(f"prediction result is {pred_result}")
                _update_comment_result(pred_result, comment)
                logger.info("updated to database")
            except Exception as ex:
                logger.error(ex)


def _parse_limit_token(content):
    tokens = content.split()
    return " ".join(tokens[:100])


def _predict(content):
    label = ["NEG", "POS", "NEU"]

    model = RobertaForSequenceClassification.from_pretrained(
        "./sentiment/phobert-base-vietnamese-sentiment"
    )  # noqa

    tokenizer = AutoTokenizer.from_pretrained(
        "./sentiment/phobert-base-vietnamese-sentiment", use_fast=False
    )  # noqa

    input_ids = torch.tensor([tokenizer.encode(content)])

    with torch.no_grad():
        out = model(input_ids)
        output = out.logits.softmax(dim=-1).tolist()[0]
        predict = label[output.index(max(output))]
        if predict == "NEU":
            predict = "POS"
        return predict


def _update_comment_result(pred_result: str, comment: Comment):
    comment_in: CommentUpdate = CommentUpdate.from_orm(comment)

    comment_in.model_prediction = pred_result

    comparing_rating = "NEG"

    if comment_in.rating >= 5:
        comparing_rating = "POS"

    comment_in.need_review = not (comparing_rating == pred_result)
    logger.info(f"comment need review is {comment_in.need_review}")

    repo.update_comment(comment_in)

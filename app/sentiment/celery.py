import shared.config as cfg
from celery import Celery

app = Celery("sentiment", include=["sentiment.tasks"])

app.config_from_object("sentiment.celeryconfig")

app.conf.beat_schedule = {
    "run-sentiment-schedule": {
        "task": "sentiment.tasks.sentiment_analyze_task",
        "schedule": int(cfg.schedule),
    },
}

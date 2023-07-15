from .celery import app

app.send_task(
    "sentiment.tasks.sentiment_analyze_task",
    kwargs={"commentid": "e83d0227-5d91-4855-a83c-c955215d4079"},
)
app.send_task(
    "sentiment.tasks.sentiment_analyze_task",
    kwargs={"commentid": "ff32e4b0-6bdc-4040-bc04-ebc93286eabe"},
)

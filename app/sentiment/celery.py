from celery import Celery

app = Celery('sentiment',
             broker='pyamqp://guest@rabbitmq//',
             include=['sentiment.tasks'])

from celery import Celery
from .config import BROKER, BACKEND


celery_app = Celery('test', broker=BROKER, backend=BACKEND, include=['app.celery_task.tasks'])

from .celery import celery_app
from app.core.redis import redis_client
import time


@celery_app.task
def test_task():
    a = 1
    b = 2
    print(a+b)
    return a+b


@celery_app.task
def savefile2redis(filename, s, deadline=3600):
    # time.sleep(10)
    redis_client.set(filename, s)
    print("wdazxzxzxzx")
    redis_client.expire(filename, deadline)
    return filename

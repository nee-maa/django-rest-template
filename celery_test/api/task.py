import json

from django_redis import get_redis_connection

from celery_test.celery import app
from celery import shared_task
from django.contrib.auth.models import User


@shared_task
def send_notification(product_code, product_name):
    con = get_redis_connection("default")
    users = con.hgetall(product_code)
    with open("emails.txt", "a+") as file:
        for k, v in users.items():
            v = json.loads(v.decode())
            file.write("Email: {} >>> message: Hi Dear {} {}. The {} now is exist in shop.\n"
                       .format(v[0], v[1], v[2], product_name))
    return None

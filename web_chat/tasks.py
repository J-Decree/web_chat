from celery.task import task
from util.email import EmailHelper
# from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_chat.settings')
app = Celery('web_chat')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task(bind=True, max_retries=3, default_retry_delay=10)
def async_email(self, email):
    """
    1.bind：是否绑定到Celery类中。绑定到类中，可以使用其他相关的方法
    2.max_retries：最多尝试执行的次数
    3.default_retry_delay：尝试执行的等待时间
    """
    try:
        email_helper = EmailHelper()
        status = email_helper.send_captcha(receive_email=email)
        return status
    except Exception as e:
        raise self.retry(exc=e)


import time


@task(bind=True, max_retries=3, default_retry_delay=10)
def t(self, a, b):
    try:
        time.sleep(15)
        print('ddd' * 10)
        c = a + b
    except Exception as e:
        raise self.retry(exc=e)
    return c


@app.task
def add(x, y):
    return x + y

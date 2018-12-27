import time
import hashlib
from django_redis import get_redis_connection


def create_token(source=''):
    ctime = str(time.time())
    m = hashlib.md5(bytes(ctime, encoding='utf8'))
    m.update(bytes(source, encoding='utf8'))
    return m.hexdigest()


class CaptchaHelper(object):
    def __init__(self):
        self.conn = get_redis_connection('default')

    @staticmethod
    def create_captcha(captcha_length=6):
        return create_token()[:captcha_length]

    def create_and_save_captcha(self, email, ex=1200):
        """
        存储验证码到redis数据库里面。
        example: 'captcha_973697101@qq.com':'e3dsf1'
        :param email: 
        :param captcha: 
        :return: 
        """
        captcha = self.create_captcha()
        key = '_'.join(['captcha', email])
        self.conn.set(key, captcha, ex=ex)
        return captcha

    def get_captcha_by_email(self, email):
        key = '_'.join(['captcha', email])
        return self.conn.get(key)

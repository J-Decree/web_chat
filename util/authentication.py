from django_redis import get_redis_connection
from chat.models import UserInfo
from .verify_code import create_token

CONN_KEY = 'default'
EX = 24 * 60 * 60  # 经过多少秒过期


class TokenHelper(object):
    def __init__(self):
        self.conn = get_redis_connection(CONN_KEY)
        self.token = None

    def set_token_by_qq(self, qq):
        self.token = create_token(qq)
        self.conn.set(qq, self.token, ex=EX)
        self.conn.set(self.token, qq, ex=EX)

    def delete_token(self, token):
        qq = self.conn.get(token) or ''
        self.conn.delete(qq)
        self.conn.delete(token)

    def reset_token_by_qq(self, qq):
        token = self.conn.get(qq) or ''
        self.delete_token(token)
        self.set_token_by_qq(qq)

    def find_token(self, token):
        return self.conn.get(token)

    def get_qq_by_token(self, token):
        return self.find_token(token)


def qq_authenticate(qq, password):
    userinfo = UserInfo.default_objects.get(qq=qq)
    if userinfo.user.check_password(password):
        return userinfo
    else:
        raise UserInfo.DoesNotExist

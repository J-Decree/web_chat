from django_redis import get_redis_connection

QQ_KEY = 'qq'
QQ_VALUE_START = '10000000'


class QQSource(object):
    def __init__(self, conn_key):
        self.conn = get_redis_connection(conn_key)
        self.conn.set(QQ_KEY, QQ_VALUE_START, nx=True)

    def get_new_qq(self):
        qq = self.conn.get(QQ_KEY)
        self.conn.incr(QQ_KEY)
        return qq

    def get_now_qq(self):
        return self.conn.get(QQ_KEY)


qq_source = QQSource(conn_key='default')

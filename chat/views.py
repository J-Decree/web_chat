from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models


# Create your api_views here.
def chat(request, **kwargs):
    models.User.objects.create(username='事务测试对象', password='juedui11')
    a = 1 / 0
    models.User.objects.create(username='事务测试对象2', password='juedui11')
    return render(request, 'chat/chat.html')


class TestCookieView(APIView):
    authentication_classes = []

    def get(self, request, **kwargs):
        qq = request.COOKIES.get('qq')
        print(request.COOKIES, '*' * 100)
        print(qq, '*' * 100)
        a = HttpResponse(qq)
        a.set_cookie('fuck', 'XXXXXXXX')
        return a


class TestRedisView(APIView):
    authentication_classes = []
    from django_redis import get_redis_connection
    conn = get_redis_connection('default')

    def get(self, request, **kwargs):
        # 获得hash全部值
        # hash_key = 'test_hash_1_15'
        # res = self.conn.hgetall(hash_key)
        # for k, v in res.items():
        #     print(k, v)

        # hask_key = 'test666'
        # res = self.conn.hget(hask_key, 'd')  # 取出来的是json字符串
        # print(type(res), res)

        for item in self.conn.scan_iter('test_hash_1_*', count=10):
            d = self.conn.hgetall(item)
            print(d)
        return Response({})

    def post(self, request, **kwargs):
        # hash_key = 'test666'
        # d = {'love': '多对多', 'age': 111, 'l': [1, 23, {1, 3, 4}, {'11': 'ffff'}]}
        # l = ['freedom', 111, 'dddddd', d]
        # self.conn.hmset(hash_key, {'title': '我爱的', 'config': d, 'datas': l, 'd': {1: '1', 2: '2'}})
        # self.conn.hset(hash_key, 'd', '时代风帆大厦')

        # 结论,API方法会帮你将列表，字典转化为字符串，无论递归到多深也不怕

        a = self.conn.set('666', 'test')
        return Response({'dd': a})


class TestRedisListView(APIView):
    """
    测试 redis对阻塞队列
    """
    authentication_classes = []
    from django_redis import get_redis_connection
    conn = get_redis_connection('default')

    def get(self, request, **kwargs):
        list_key = 'list666'
        res = self.conn.blpop(list_key, timeout=10)
        return Response({'data': res})

    def post(self, request, **kwargs):
        list_key = 'list666'
        value = request.data['value']
        self.conn.lpush(list_key, value)
        return Response({})


def url_test(request, **kwargs):
    print('request.path_info->路径', request.path_info)
    print('request.get_full_path()->路径加路径的参数', request.get_full_path())
    print('request.get_all_path()->获取带参数URL',request.get_all_path())
    print('request.path->获取不带参数URL',request.path)
    print('request.get_host()->获取主机地址',request.get_host())
    return HttpResponse('dddd')

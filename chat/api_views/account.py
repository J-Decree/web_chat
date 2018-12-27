import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from util.authentication import TokenHelper, qq_authenticate
from django.contrib.auth.models import User
from util.api import APIResponse
from django.db import IntegrityError
from chat import models
from web_chat.tasks import async_email

logger = logging.getLogger('django')


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, **kwargs):
        response = APIResponse()
        token_helper = TokenHelper()
        try:
            qq = request.data['qq']
            password = request.data['password']
            qq_authenticate(qq=qq, password=password)
            token_helper.reset_token_by_qq(qq=qq)
            response.token = token_helper.token
        except models.UserInfo.DoesNotExist:
            response.code = 1001
            response.error = '用户名或密码不存在'
        except Exception as e:
            print(e)
            response.code = 1003
            response.error = '请求参数不正确'
        return Response(response.dict)


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request, **kwargs):
        response = APIResponse()
        try:
            username = request.data['username']
            password = request.data['password']
            user = User.objects.create(username=username, password=password)
            response.data = user.userinfo.qq
        except IntegrityError:
            response.code = 1001
            response.error = '用户名已经存在'
        except:
            response.code = 1003
            response.error = '请求参数不正确'
        return Response(response.dict)


class LogoutView(APIView):
    def get(self, request, **kwargs):
        response = APIResponse()
        token_helper = TokenHelper()
        try:
            token = request.GET['token']
            token_helper.delete_token(token=token)
            response.message = '退出成功'
        except Exception as e:
            print(e)
            response.code = 1003
            response.error = '请求参数不正确'
        return Response(response.dict)


class EmailCaptchaView(APIView):
    authentication_classes = []

    def post(self, request, **kwargs):
        response = APIResponse()
        try:
            email = request.data['email']
            async_email.delay(email)
        except KeyError:
            response.error = 1001
            response.error = '请求参数不正确'
        except Exception as e:
            logger.error('发送邮件失败,错误为:%s' % str(e))
            response.error = 1003
            response.error = '服务器异常'
        return Response(response.dict)

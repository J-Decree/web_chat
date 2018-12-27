from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from util.authentication import TokenHelper
from chat import models


class ChatAuthentication(BaseAuthentication):
    token_helper = TokenHelper()

    def authenticate(self, request):
        token = request.GET.get('token', '')
        if not self.token_helper.find_token(token):
            raise exceptions.AuthenticationFailed('用户认证失败')
        qq = self.token_helper.get_qq_by_token(token)
        userinfo = models.UserInfo.default_objects.filter(qq=qq).first()
        if not userinfo:
            raise exceptions.AuthenticationFailed('用户不存在')
        return userinfo.user, token

    def authenticate_header(self, request):
        pass

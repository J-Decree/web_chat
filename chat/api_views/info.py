from rest_framework.views import APIView
from rest_framework.response import Response
from chat.rest_components.serializers.info import UserInfoSerializer, WebGroupSerializer
from util.api import APIResponse
from chat.models import UserInfo, WebGroupInfo


class UserInfoView(APIView):
    def get(self, request, **kwargs):
        response = APIResponse()
        try:
            userinfo = request.user.userinfo
            ser = UserInfoSerializer(instance=userinfo, many=False)
            response.data = ser.data
        except:
            response.code = 1003
            response.error = '系统错误'
        return Response(response.dict)


class FriendsView(APIView):
    def get(self, request, **kwargs):
        response = APIResponse()
        try:
            userinfo = request.user.userinfo
            friends = userinfo.friends.all()
            ser = UserInfoSerializer(instance=friends, many=True)
            response.data = ser.data
        except:
            response.code = 1003
            response.error = '系统错误'
        return Response(response.dict)


class GroupsView(APIView):
    def get(self, request, **kwargs):
        response = APIResponse()
        try:
            userinfo = request.user.userinfo
            groups = userinfo.as_members_groups_set.all()
            ser = WebGroupSerializer(instance=groups, many=True)
            response.data = ser.data
        except Exception as e:
            print(e)
            response.code = 1003
            response.error = '系统错误'
        return Response(response.dict)

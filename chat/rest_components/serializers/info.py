from rest_framework import serializers
from chat import models
from util.file import create_file_url


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        fields = ['id', 'signature', 'qq', 'avatar', 'username']
        # fields = '__all__'
        depth = 1

    def get_avatar(self, obj):
        return create_file_url(obj.avatar)


class WebGroupSerializer(serializers.ModelSerializer):
    """
    传入 userinfo.as_member_groups_set，序列化组
    """
    avatar = serializers.SerializerMethodField()

    # admins = serializers.SerializerMethodField()
    # members = serializers.SerializerMethodField()

    class Meta:
        model = models.WebGroupInfo
        fields = ['id', 'title', 'admins', 'members', 'creator', 'avatar']
        depth = 0

    def get_avatar(self, obj):
        return create_file_url(obj.avatar)

        # def get_admins(self, obj):
        #     ser = UserInfoSerializer(instance=obj.admins, many=True)
        #     return ser.data
        #
        # def get_members(self, obj):
        #     ser = UserInfoSerializer(instance=obj.members, many=True)
        #     return ser.data

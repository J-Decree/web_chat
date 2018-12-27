import queue
from chat.models import UserInfo, WebGroupInfo
from .message import QueueMessage


class BaseQueue(object):
    def __init__(self, key_set):
        self.site = {}
        self.__init_site(key_set)

    def __init_site(self, key_set):
        for key in key_set:
            self.site[key] = queue.Queue()


class MessageQueue(BaseQueue):
    def __init__(self):
        query_set = UserInfo.objects.all()
        id_list = [obj.id for obj in query_set]
        super(MessageQueue, self).__init__(id_list)

    def publish(self, userinfo_set, message: QueueMessage):
        for userinfo in userinfo_set:
            self.site[userinfo.id].put(message.to_json())

    def publish_to_friend(self, friend_id, message: QueueMessage):
        """
        :param friend_id: 朋友的id 
        :return: 
        """
        print(self.site, friend_id)
        self.site[friend_id].put(message.to_json())

    def publish_to_group(self, group_id, message: QueueMessage, exclude_id=None):
        """
        :param group_id: 
        :param message: 
        :param exclude_id: 发送到群，要排除自己发送给自己到情况 
        :return: 
        """
        group = WebGroupInfo.default_objects.get(id=group_id)
        members_set = group.members.exclude(id=exclude_id)
        self.publish(members_set, message)

    def publish_login_message(self, userinfo_id):
        """
        :param userinfo_id: 登录用户自己的id 
        :return: 
        """
        message = QueueMessage()
        message.as_login_message(userinfo_id=userinfo_id)
        useinfo = UserInfo.default_objects.get(id=userinfo_id)
        friends_set = useinfo.friends.all()
        self.publish(friends_set, message)

    def publish_logout_message(self, userinfo_id):
        message = QueueMessage()
        message.as_logout_message(userinfo_id=userinfo_id)
        useinfo = UserInfo.default_objects.get(id=userinfo_id)
        friends_set = useinfo.friends.all()
        self.publish(friends_set, message)


class HeartbeatQueue(MessageQueue):
    pass


message_queue = MessageQueue()
heartbeat_queue = MessageQueue()

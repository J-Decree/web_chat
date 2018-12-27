import json

# target_type,trigger_type
FRIENDS_MESSAGE = 'friend'
GROUPS_MESSAGE = 'group'

# content_type
SIMPLE_CONTENT = 'text'
FILE_CONTENT = 'file'
IMAGE_CONTENT = 'image'
SYSTEM_CONTENT = 'system'
ACCOUNT_CONTENT = 'account'  # content = 0 为下线， content = 1为上线

LOGIN_CONTENT = 1
LOGOUT_CONTENT = 0


class BaseMessage(object):
    @property
    def dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.dict)


class QueueMessage(BaseMessage):
    """
    放进用户队列里面的消息
    """

    def __init__(self, trigger=None, trigger_type=FRIENDS_MESSAGE,
                 content=None, content_type=SIMPLE_CONTENT):
        self.trigger = trigger  # 用户信息id or 群id
        self.trigger_type = trigger_type
        self.content = content
        self.content_type = content_type

    def as_login_message(self, userinfo_id):
        self.trigger = userinfo_id
        self.trigger_type = FRIENDS_MESSAGE
        self.content = LOGIN_CONTENT
        self.content_type = ACCOUNT_CONTENT

    def as_logout_message(self, userinfo_id):
        self.as_login_message(userinfo_id)
        self.content = LOGOUT_CONTENT

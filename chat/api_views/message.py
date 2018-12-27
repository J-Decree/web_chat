import queue
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from util.queue import message_queue, heartbeat_queue
from util.api import APIResponse
from util import message


class MessageView(APIView):
    def get(self, request, **kwargs):
        """
        用户每次过来查询自己key为userinfo.id的queue的队列消息,hold住5秒
        :param request: 
        :param kwargs: 
        :return: 
        """
        response = APIResponse()
        try:
            userinfo = request.user.userinfo
            q = message_queue.site[userinfo.id]
            data = q.get(timeout=5)
            response.data = json.loads(data)
        except queue.Empty:
            response.code = 1001
            response.error = '暂时无数据'
        except Exception:
            response.code = 1003
            response.error = '系统错误'
        return Response(response.dict)

    def post(self, request, **kwargs):
        """
        解析用户提交的POST数据,存入相应的队列
        
        传递过来的有
        
        根据传过来的target_type和target。转换为BaseMessage存入队列
        :param request: 
        :param kwargs: 
        :return: 
        """
        response = APIResponse()
        try:
            userinfo = request.user.userinfo
            userinfo_id = userinfo.id
            content = request.data['content']
            content_type = request.data['content_type']
            target = request.data['target']
            target_type = request.data['target_type']
            target = int(target)
            if target_type == message.FRIENDS_MESSAGE:
                # 发送给朋友
                queue_message = message.QueueMessage(trigger=userinfo_id, content=content, content_type=content_type)
                message_queue.publish_to_friend(friend_id=target, message=queue_message)
                ack_message = message.QueueMessage(trigger=target, content=content, content_type=content_type)
                response.data = ack_message.dict
            elif target_type == message.GROUPS_MESSAGE:
                # 发送给群
                queue_message = message.QueueMessage(trigger=target, trigger_type=message.GROUPS_MESSAGE,
                                                     content=content,
                                                     content_type=content_type)
                message_queue.publish_to_group(group_id=target, message=queue_message, exclude_id=userinfo_id)
                ack_message = message.QueueMessage(trigger=target, trigger_type=message.GROUPS_MESSAGE,
                                                   content=content, content_type=content_type)
                response.data = ack_message.dict
            else:
                raise Exception('不在处理范围之内')
        except Exception as e:
            response.code = 1003
            response.error = '发生未知错误'
        return Response(response.dict)


class HeartBeatView(APIView):
    def get(self, request, **kwargs):
        response = APIResponse()
        try:
            useinfo_id = request.user.userinfo.id
            heartbeat_queue.site[useinfo_id].put(useinfo_id)
            response.message = 'success'
        except Exception:
            response.code = 1003
            response.error = '未知错误'
        return Response(response.dict)

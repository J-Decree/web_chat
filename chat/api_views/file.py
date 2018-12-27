import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from chat.rest_components.serializers.uploads import FileSerializer, ImageSerializer
from util.api import APIResponse
from util.file import check_or_create_folder, save_file, create_file_url, format_file_size
from util import message
from util.queue import message_queue


# class UploadView(APIView):
#     parser_classes = [FileUploadParser]
#     folder = 'file'
#     upload_folder = os.path.join(settings.MEDIA_ROOT, folder)
#     check_or_create_folder(upload_folder)
#
#     def post(self, request, **kwargs):
#         userinfo = request.user.userinfo
#         qq = userinfo.qq
#         response = APIResponse()
#         file_obj = request.data['file']
#         filename = qq + '_' + file_obj.name
#         file_path = os.path.join(self.upload_folder, filename)
#         save_file(file_path=file_path, file_obj=file_obj)
#         return Response(response.dict)


class UploadView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    folder = 'file'
    content_type = message.FILE_CONTENT
    validate_ser = FileSerializer

    def post(self, request, **kwargs):
        upload_folder = os.path.join(settings.MEDIA_ROOT, self.folder)
        check_or_create_folder(upload_folder)
        # #先存储好文件
        response = APIResponse()
        file_obj = None
        try:
            userinfo = request.user.userinfo
            userinfo_id = userinfo.id
            qq = userinfo.qq
            # file_obj = request.FILES['file']
            # # 验证文件是否合乎类型
            ser = self.validate_ser(data=request.FILES)
            if ser.is_valid():
                file_obj = ser.validated_data['file']
            else:
                raise Exception('请上传正确的图片文件')

            filename = qq + '_' + file_obj.name
            file_path = os.path.join(upload_folder, filename)
            file_url = os.path.join(self.folder, filename)
            save_file(file_path=file_path, file_obj=file_obj)
            # #生成链接返回给客户端
            url = create_file_url(file_url)
            # #发送消息到相关队列
            target = request.data['target']
            target_type = request.data['target_type']
            target = int(target)
            content = {
                'url': url,
                'filename': file_obj.name,
                'status': '发送成功',
                'size': format_file_size(file_obj.size)
            }
            if target_type == message.FRIENDS_MESSAGE:
                # 发送给朋友
                queue_message = message.QueueMessage(trigger=userinfo_id, content=content,
                                                     content_type=self.content_type)
                message_queue.publish_to_friend(friend_id=target, message=queue_message)
                ack_message = message.QueueMessage(trigger=target, content=content, content_type=self.content_type)
                response.data = ack_message.dict
            elif target_type == message.GROUPS_MESSAGE:
                # 发送给群
                queue_message = message.QueueMessage(trigger=target, trigger_type=message.GROUPS_MESSAGE,
                                                     content=content,
                                                     content_type=self.content_type)
                message_queue.publish_to_group(group_id=target, message=queue_message, exclude_id=userinfo_id)
                ack_message = message.QueueMessage(trigger=target, trigger_type=message.GROUPS_MESSAGE,
                                                   content=content, content_type=self.content_type)
                response.data = ack_message.dict
            else:
                raise Exception('不在处理范围之内')
        except Exception as e:
            response.code = 1003
            response.error = str(e)
        return Response(response.dict)


class UploadImageView(UploadView):
    folder = 'image'
    content_type = message.IMAGE_CONTENT
    validate_ser = ImageSerializer

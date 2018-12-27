from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(error_messages={'blank': '文件不能为空'})


class ImageSerializer(serializers.Serializer):
    file = serializers.ImageField(error_messages={'blank': '文件不能为空'})

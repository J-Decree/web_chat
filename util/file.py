import os
from django.conf import settings


def check_or_create_folder(upload_folder):
    print(upload_folder, '*' * 100)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


def save_file(file_path, file_obj):
    with open(file_path, 'wb') as f:
        for line in file_obj:
            f.write(line)


def create_file_url(file_name):
    file_name = str(file_name)
    ret = settings.HOST + os.path.join(settings.MEDIA_URL, file_name) if file_name else None
    return ret


def format_file_size(size):
    """
    如果 size<1024 则返回 B 为单位的数据
    如果size>1024 则返回 KB 为单位的数据
    如果size>1024*1024 则返回 MB 为单位的数据
    :param size: 文件大小，单位是比特 
    :return: 
    """
    if size > 1024 * 1024:
        return '%s MB' % round(size / 1024 / 1024, 1)
    elif size > 1024:
        return '%s KB' % round(size / 1024, 1)
    else:
        return '%s Bytes' % size

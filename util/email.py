import time
from django.conf import settings
from django.core.mail import send_mail
from chat.models import EmailVerifyRecord
from .verify_code import CaptchaHelper


class EmailHelper(object):
    def __init__(self):
        self.email_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.email_from = settings.EMAIL_FROM  # 发送人

    def send_captcha(self, receive_email):
        """
        发送验证码
        """
        captcha_helper = CaptchaHelper()
        captcha = captcha_helper.create_and_save_captcha(email=receive_email)
        # 邮件发送参数
        email_title = '修仔科技'
        email_body = '%s' % (captcha,)
        status = send_mail(email_title, email_body, self.email_from, [self.email_from, receive_email])
        return status

    def set_user_activate_link(self):
        """
        发送注册后的激活邮件
        :return: 
        """
        pass

    def send_password_reset_link(self):
        """
        发送密码重置链接
        :return: 
        """

    def send_email_reset_link(self):
        """
        发送邮箱重置链接
        :return: 
        """

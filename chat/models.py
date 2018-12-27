from datetime import datetime
from util.source import qq_source

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class MyCustomManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(MyCustomManager, self).get_queryset().filter(isDelete=False)


custom_manager = MyCustomManager()


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    isDelete = models.BooleanField(verbose_name='是否已经删除', default=False)

    default_objects = models.Manager()  # objects = BaseManger会被覆盖
    objects = custom_manager

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.isDelete = True
        self.save()
        print('isDelete = false')


def upload_to(instance, filename):
    from util.authentication import create_token
    token = create_token()
    filename = '%s%s' % (token, filename)
    return '/'.join(['head', filename])


class UserInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    signature = models.CharField(max_length=32, blank=True, null=True)
    friends = models.ManyToManyField('self', verbose_name='好友们', null=True, blank=True,
                                     related_name='as_friends_userinfo_set')
    avatar = models.ImageField(verbose_name='头像', default='head/3.png',
                               upload_to=upload_to)
    qq = models.CharField(max_length=12, verbose_name='qq号码', unique=True)
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, unique=True)  # 测试，和业务无关

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        qq = qq_source.get_new_qq()
        u = UserInfo.objects.create(user=instance, qq=qq)
        u.save()
        print('create_user!!!!!!!!!!!!!!!!')


@receiver(post_delete, sender=User)
def delete_comment_after(sender, instance, **kwargs):
    # 这里报错，因为User对象是真删，UserInfo是假删
    instance.userinfo.delete()


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     qq = qq_source.get_new_qq()
#     instance.qq = qq
#     instance.userinfo.save()
#     print('save_user!!!!!!!!!!!!!!!!')


class WebGroupInfo(BaseModel):
    title = models.CharField(max_length=16, verbose_name='群名字')
    admins = models.ManyToManyField('UserInfo', verbose_name='管理员们', related_name='as_admin_groups_set')
    members = models.ManyToManyField('UserInfo', verbose_name='群人员们', related_name='as_members_groups_set')
    creator = models.ForeignKey('UserInfo', verbose_name='创建者', related_name='as_creator_groups_set')
    avatar = models.ImageField(verbose_name='群头像', default='head/3.png',
                               upload_to=upload_to)

    def __str__(self):
        return self.title


class EmailVerifyRecord(models.Model):
    """
    这个是为了可以通过url后缀随机字符串找出对应的邮箱，进而找出对应的用户
    """
    send_type_choices = [("active_link", u"注册激活"), ("reset_password", u"重置密码"),
                         ("update_email", u"修改邮箱")]
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=send_type_choices, max_length=30)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码(url标志)"
        verbose_name_plural = verbose_name

    def get_user_by_code(self, code):
        query_set = self.objects.filter(code=code).order_by('-send_time').all()
        if query_set:
            record = query_set.first()
            user = UserInfo.objects.filter(email=record.email)
            return user

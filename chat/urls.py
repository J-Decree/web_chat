from django.conf.urls import url
from .api_views import account, info, message, file
from chat import views

urlpatterns = [
    url(r'^(?P<version>[V1|v2]+)/login/$', account.LoginView.as_view()),
    url(r'^(?P<version>[V1|v2]+)/logout/$', account.LogoutView.as_view()),
    url(r'^(?P<version>[V1|v2]+)/register/$', account.RegisterView.as_view()),
    url(r'(?P<version>[V1|v2]+)/captcha/$', account.EmailCaptchaView.as_view()),

    url(r'^(?P<version>[V1|v2]+)/userinfo/$', info.UserInfoView.as_view()),
    url(r'^(?P<version>[V1|v2]+)/friends/$', info.FriendsView.as_view()),
    url(r'^(?P<version>[V1|v2]+)/groups/$', info.GroupsView.as_view()),

    url(r'^(?P<version>[V1|v2]+)/message/$', message.MessageView.as_view()),
    url(r'^(?P<version>[V1|v2]+)/heartbeat/$', message.HeartBeatView.as_view()),

    url(r'(?P<version>[V1|v2]+)/file/$', file.UploadView.as_view()),
    url(r'(?P<version>[V1|v2]+)/image/$', file.UploadImageView.as_view()),
    url(r'(?P<version>[V1|v2]+)/test/$', views.TestRedisListView.as_view()),
    url(r'(?P<version>[V1|v2]+)/test2/$', views.TestRedisView.as_view()),
]

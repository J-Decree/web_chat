# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-12-19 14:15
from __future__ import unicode_literals

import chat.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('simple', '普通验证码'), ('active_link', '注册激活'), ('reset_password', '重置密码'), ('update_email', '修改邮箱')], max_length=30, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否已经删除')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('signature', models.CharField(blank=True, max_length=32, null=True)),
                ('avatar', models.ImageField(default='head/3.png', upload_to=chat.models.upload_to, verbose_name='头像')),
                ('qq', models.CharField(max_length=12, unique=True, verbose_name='qq号码')),
                ('email', models.EmailField(default=None, max_length=32, null=True, verbose_name='邮箱')),
                ('friends', models.ManyToManyField(blank=True, null=True, related_name='_userinfo_friends_+', to='chat.UserInfo', verbose_name='好友们')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WebGroupInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否已经删除')),
                ('title', models.CharField(max_length=16, verbose_name='群名字')),
                ('avatar', models.ImageField(default='head/3.png', upload_to=chat.models.upload_to, verbose_name='群头像')),
                ('admins', models.ManyToManyField(related_name='as_admin_groups_set', to='chat.UserInfo', verbose_name='管理员们')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_creator_groups_set', to='chat.UserInfo', verbose_name='创建者')),
                ('members', models.ManyToManyField(related_name='as_members_groups_set', to='chat.UserInfo', verbose_name='群人员们')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

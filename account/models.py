#coding=utf-8

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    ip = models.IPAddressField(verbose_name=u'ip地址')
    time = models.DateTimeField(verbose_name=u'提交时间')
    nickname = models.CharField(verbose_name=u'昵称', max_length=30)

    def __unicode__(self):
        return self.nickname

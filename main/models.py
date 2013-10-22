#coding=utf-8

from django.db import models
from django.contrib.auth.models import User

item_status = (
               (0, u'未审核'),
               (1, u'已审核'),
               (2, u'丢弃'),
               )

user_record_action = (
                      (0,u'赞成'),
                      (1,u'反对'),
                      )

class Item(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    context = models.TextField(verbose_name=u'内容')
    time = models.DateTimeField(verbose_name=u'提交时间')
    agree = models.PositiveIntegerField(verbose_name=u'赞', default=0)
    disagree = models.PositiveIntegerField(verbose_name=u'贬', default=0)
    score = models.IntegerField(verbose_name=u'积分', default=0)
    image = models.ImageField(verbose_name=u'图片', upload_to='image/item', blank=True, null=True)
    status = models.PositiveIntegerField(verbose_name=u'状态', choices=item_status, default=0)
    comments = models.PositiveIntegerField(verbose_name=u'评论', default=0)
    
    def __unicode__(self):
        return u'%s' % self.id
    
class Comment(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    context = models.CharField(verbose_name=u'内容', max_length=100)
    time = models.DateTimeField(verbose_name=u'提交时间')
    
    def __unicode__(self):
        return u'%s' % self.id
    
class User_Record(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    action = models.PositiveIntegerField(verbose_name=u'动作', choices=user_record_action, default=0)
    
    def __unicode__(self):
        return u'%s' % self.id

class Item_Ready(models.Model):
    context = models.TextField(verbose_name=u'内容')
    image = models.ImageField(verbose_name=u'图片', upload_to='image/item', blank=True, null=True)
    status = models.PositiveIntegerField(verbose_name=u'状态', choices=item_status, default=0)
    
    def __unicode__(self):
        return u'%s' % self.id

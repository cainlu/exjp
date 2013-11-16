#coding=utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from forms import UploadForm
from models import Item, User_Record, Comment, Item_Ready
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import time
import json
import random

def display(request):
    page = int(request.GET.get('page', '1'))
    items = Item.objects.filter(status=1).order_by('-score')
    pages = int((len(items) + 20 - 1) / 20)
    if len(items) > page * 20:
        items = items[(page - 1) * 20 : page * 20]
    else:
        items = items[(page - 1) * 20 :]
    return render_to_response('display.jinja', {'items':items, 'page':page, 'pages':pages}, RequestContext(request))

def upload(request):
    return render_to_response('upload.jinja', {}, RequestContext(request))

def judge_action(request):
    form = UploadForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        context = data['context']
        if '_auth_user_id' in request.session:
            user_id = request.session['_auth_user_id']
            user = User.objects.get(id=user_id)
        else:
            user = None
        if request.FILES.has_key('image'):
            image = request.FILES['image']
        else:
            image = None
        if image != None and image.size > 3 * 1024 * 1024:
            return render_to_response('result.jinja', {'state':'2', 'message':u'图片最大3M', 'url':'/main/upload'}, RequestContext(request))
        item = Item.objects.create(
                                   user=user,
                                   context=context,
                                   time=datetime.now(),
                                   image=image,
                                   status=0,
                                   agree=random.randint(100, 200),
                                   disagree=random.randint(0, 50),
                                   score=int(time.time() / (60 * 60) * 1000),
                                   )
        item.save()
        return render_to_response('result.jinja', {'state':'1', 'message':u'上传成功', 'url':'/main/upload'}, RequestContext(request))
    else:
        for field in form:
            if field.errors:
                return render_to_response('result.jinja', {'state':'2', 'message':field.errors, 'url':'/main/upload'}, RequestContext(request))

def vote_action(request):
    response = HttpResponse()
    item_id = request.GET['item_id']
    action = request.GET['action']
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
        user = User.objects.get(id=user_id)
        item = Item.objects.get(id=item_id)
        user_records = User_Record.objects.filter(user_id=user_id, item_id=item_id)
        if len(user_records) > 0:
            result = json.dumps({'state':'3'})#当前用户已进行过投票
        else:
            user_record = User_Record.objects.create(
                                                     user=user,
                                                     item=item,
                                                     action=action,
                                                     )
            user_record.save()
            if action == '0':
                item.disagree += 1
                item.score -= 1000
                item.save()
                result = json.dumps({'state':'1', 'num':item.disagree})
            elif action == '1':
                item.agree += 1
                item.score += 1000
                item.save()
                result = json.dumps({'state':'1', 'num':item.agree})
    else:
        result = json.dumps({'state':'2'})#请先登录再进行操作
    response.write(result)
    return response

def comment_show(request):
    item_id = request.GET['item_id']
    comments = Comment.objects.filter(item_id=item_id).order_by('-time', '-id')
    return render_to_response('comments.jinja', {'comments':comments, 'item_id':item_id}, RequestContext(request))

def comment_action(request):
    item_id = request.GET['item_id']
    context = request.GET['context']
    if '_auth_user_id' in request.session:
        user_id = request.session['_auth_user_id']
        user = User.objects.get(id=user_id)
        item = Item.objects.get(id=item_id)
        comment_recent = Comment.objects.filter(user=user, item=item).order_by('-time')
        if len(comment_recent) == 0 or datetime.now() - comment_recent[0].time > timedelta(minutes = 1):
            comment = Comment.objects.create(
                                             user=user,
                                             item=item,
                                             context=context,
                                             time=datetime.now(),
                                             )
            comment.save()
            item.comments += 1
            item.score += 3000
            item.save()
            return render_to_response('comment_add.jinja', {'state':'1', 'comment_add':comment, 'item_id':item_id, 'comment_num':item.comments}, RequestContext(request))
        else:
            return render_to_response('comment_add.jinja', {'state':'3'}, RequestContext(request))#请过1分钟再对其进行评论
    else:
        return render_to_response('comment_add.jinja', {'state':'2'}, RequestContext(request))#请先登录再进行操作

def contact_us(request):
    return render_to_response('result.jinja', {'state':'3', 'url':'/'}, RequestContext(request))

def about_us(request):
    return render_to_response('result.jinja', {'state':'4', 'url':'/'}, RequestContext(request))

def upload_per_hour(request):
    user = request.GET['user']
    password = request.GET['password']
    if user == settings.ITEM_READY_UESR and password == settings.ITEM_READY_PASSWORD:
        user = User.objects.get(username=user)
        item_ready = Item_Ready.objects.filter(status=0).order_by('id')[0]
        item = Item.objects.create(
                                   user=None,
                                   context=item_ready.context,
                                   time=datetime.now(),
                                   image=item_ready.image,
                                   status=1,
                                   score=int(time.time() / (60 * 60) * 1000),
                                   )
        item.save()
        item_ready.status = 1
        item_ready.save()
    return HttpResponseRedirect('/')

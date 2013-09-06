#coding=utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.models import User
from forms import RegisterForm, LoginForm
from models import UserProfile
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from datetime import datetime, timedelta
import json

def register(request):
    return render_to_response('register.jinja', {}, RequestContext(request))

def register_action(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        time_now = datetime.now()
        username = data['username']
        nickname = data['nickname']
        password = data['password']
        email = data['email']
        user_profile_ip = UserProfile.objects.filter(ip=ip).order_by('-time')
        if len(user_profile_ip) == 0 or time_now - user_profile_ip[0].time > timedelta(days=1):
            user = User.objects.create_user(username=username, password=password, email=email)
            if user is not None:
                user_profile = UserProfile.objects.create(user=user, ip=ip, time=time_now, nickname=nickname)
                user.save()
                user_profile.save()
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return render_to_response('result.jinja', {'state':'1', 'message':u'注册成功', 'url':'/'}, RequestContext(request))
            else:
                return render_to_response('result.jinja', {'state':'2', 'message':u'当前用户名已存在', 'url':'/account/register'}, RequestContext(request))
        else:
            return render_to_response('result.jinja', {'state':'2', 'message':u'相同ip24小时只能注册一次', 'url':'/account/register'}, RequestContext(request))
    else:
        for field in form:
            if field.errors:
                return render_to_response('result.jinja', {'state':'2', 'message':field.errors, 'url':'/account/register'}, RequestContext(request))

def login(request):
    captcha = LoginForm()['captcha']
    return render_to_response('login.jinja', {'captcha':captcha}, RequestContext(request))

def login_action(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return render_to_response('result.jinja', {'state':'1', 'message':u'登陆成功', 'url':'/'}, RequestContext(request))
        else:
            return render_to_response('result.jinja', {'state':'2', 'message':u'用户名密码错误', 'url':'/account/login'}, RequestContext(request))
    else:
        for field in form:
            if field.errors:
                return render_to_response('result.jinja', {'state':'2', 'message':field.errors, 'url':'/account/login'}, RequestContext(request))

def logout_action(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def username_judge(request):
    response = HttpResponse()
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    time_now = datetime.now()
    username = request.GET['username']
    user = User.objects.filter(username=username)
    user_profile = UserProfile.objects.filter(ip=ip).order_by('-time')
    if len(user) > 0:
        result = json.dumps({'state':'2'})#当前用户名已存在
    elif len(user_profile) > 0 and time_now - user_profile[0].time <= timedelta(days=1):
        result = json.dumps({'state':'3'})#相同ip24小时只能注册一次
    else:
        result = json.dumps({'state':'1'})
    response.write(result)
    return response

def nickname_judge(request):
    response = HttpResponse()
    nickname = request.GET['nickname']
    user_profile = UserProfile.objects.filter(nickname=nickname)
    if len(user_profile) > 0:
        result = json.dumps({'state':'2'})#当前昵称已存在
    else:
        result = json.dumps({'state':'1'})
    response.write(result)
    return response

def captcha_judge(request):
    response = HttpResponse()
    captcha_0 = request.GET['captcha_0']
    captcha_1 = request.GET['captcha_1'].lower()
    captcha = CaptchaStore.objects.filter(hashkey=captcha_0)
    if len(captcha) > 0 and captcha[0].response == captcha_1:
        result = json.dumps({'state':'1'})
    else:
        result = json.dumps({'state':'2'})
    response.write(result)
    return response

def captcha_refresh(request):
    response = HttpResponse()
    new_captcha_key = CaptchaStore.generate_key()
    new_captcha_image = captcha_image_url(new_captcha_key)
    new_captcha_hashkey = new_captcha_image.split('/')[3]
    result = json.dumps({'state':'1', 'new_captcha_image':new_captcha_image, \
                         'new_captcha_hashkey':new_captcha_hashkey})
    response.write(result)
    return response

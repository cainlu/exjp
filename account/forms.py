#coding=utf-8
from django import forms
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=20, required=True, error_messages={'invalid':u'用户名提交错误'})
    nickname = forms.CharField(label=u'昵称', max_length=20, required=True, error_messages={'invalid':u'昵称提交错误'})
    password = forms.CharField(label=u'密码', max_length=20, required=True, widget=forms.PasswordInput, error_messages={'invalid':u'密码提交错误'})
    email = forms.EmailField(label=u'邮件地址', required=True, error_messages={'invalid':u'email提交错误'})

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名', max_length=30, required=True, error_messages={'invalid':u'用户名提交错误'})
    password = forms.CharField(label=u'密码', max_length=20, required=True, widget=forms.PasswordInput, error_messages={'invalid':u'密码提交错误'})
    captcha = CaptchaField(label=u'验证码', required=True, error_messages={'invalid':u'验证码提交错误'})

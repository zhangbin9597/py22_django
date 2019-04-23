import re
from django import http
from django.contrib.auth import login

from users.models import User
from django.shortcuts import render,redirect
from django.views import View
from meido_mall.utils.response_code import RETCODE
# Create your views here.



class register(View):

    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        # 1.接收
        user_name=request.POST.get('user_name')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')
        phone=request.POST.get('phone')
        allow=request.POST.get('allow')
        # 验证
        # 非空
        if not all([user_name,pwd,cpwd,phone,allow]):
            return http.HttpResponseBadRequest('参数不能为空')
        # 用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', user_name):
            return http.HttpResponseBadRequest('请输入5-20位字符')
        if User.objects.filter(username=user_name).count()>0:
            return http.HttpResponseBadRequest('用户名已经存在')
        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseBadRequest('请输入5-20位字符')
        if pwd!=cpwd:
            return http.HttpResponseBadRequest('两次密码必须一致')
        # 手机号
        if not re.match('^1[345789]\d{9}$', phone):
            return http.HttpResponseBadRequest('您输入的手机号格式不正确')
        if User.objects.filter(mobile=phone).count()>0:
            return http.HttpResponseBadRequest('手机号已经存在')

        # 处理
        # 3.1创建用户对象，保存到表中，先将密码加密，再保存到表中
        user = User.objects.create_user(username=user_name,password=pwd,mobile=phone)

        # 3.2状态保持
        login(request,user)
        # 响应
        return redirect('index.html')

# class IndexView(View):
#     def get(self,request):
#         return render(request,'index.html')


class UsernameCountView(View):
    def get(self, request, username):
        # 接收
        # 验证
        # 处理：查询判断
        count = User.objects.filter(username=username).count()
        # 响应：如果是ajax请求，则返回json数据
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        })
class MobileCountView(View):
    def get(self, request, mobile):
        # 接收
        # 验证
        # 处理：查询统计
        count = User.objects.filter(mobile=mobile).count()

        # 响应
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        })



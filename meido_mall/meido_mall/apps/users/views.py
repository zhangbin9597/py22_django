import re
from django import http
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse

from users.models import User
from django.shortcuts import render,redirect
from django.views import View
from meido_mall.utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin
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
        next_url = request.GET.get('next','/')
        # 3.2状态保持
        login(request,user)
        # 向cookie中输出用户名,用于在前端提示登录状态
        response = redirect(next_url)
        response.set_cookie('username',user.username,max_age=60 * 60 *24 *14)
        return response
        # 响应
        # return redirect('/index.html')
        # return redirect(reverse('users:index'))
class IndexView(View):
    def get(self,request):
        return render(request, 'index.html')


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

class LoginView(View):
    # 用户登录
    def get(self,request):

        return render(request, 'login.html')

    def post(self,request):
        # 接受参数
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        remembered = request.POST.get('remembered')
        # 接收重定向
        next_url = request.GET.get('next','/')
        # 验证参数
        if not all([username,pwd]):
            return http.HttpResponseBadRequest('请输入用户名和密码')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        user = authenticate(username=username, password=pwd)
        if remembered != 'on':
            # 没有记住用户:浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户:None表示两周后过期
            request.session.set_expiry(None)
        if user is None:
            return render(request, 'login.html', {'account_errmsg':'用户名或密码错误'})
        else:
            # 实现状态保持
            login(request,user)
            # 向cookie中输出用户名,用于在前端提示登录状态
            response = redirect(next_url)
            response.set_cookie('username',user.username,max_age=60 * 60 * 24 * 14)
            return response
            # 设置状态保存的周期

        # 响应结果
        # return redirect(reverse('users:index'))

class LogoutView(View):
    def get(self,request):
        # 清理session
        logout(request)
        response = redirect('/')
        # 退出登录时,删除cookie中的username
        response.delete_cookie('username')
        return response

class UserInfoView(LoginRequiredMixin, View):
    def get(self,request):
        # if request.user.is_authenticated:
        return render(request,'user_center_info.html')
        # else:
        #     return redirect('/login/')

import json
import re
from django import http
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.conf import settings
from users.models import User,Address
from django.shortcuts import render,redirect
from django.views import View
from meido_mall.utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin
from celery_tasks.mail.tasks import send_user_email
from meido_mall.utils import meiduo_signature
from . import contants

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
        # return render(request,'user_center_info.html')
        # else:
        #     return redirect('/login/')
    # 获取当前登录的用户
        user = request.user
        context={
            'username':user.username,
            'mobile':user.mobile,
            'email':user.email,
            'email_active':user.email_active
        }
        return render(request, 'user_center_info.html',context)

class EmailView(LoginRequiredMixin, View):
    def put(self,request):
        #接收,以put方式的请求
        dict1 = json.loads(request.body.decode())
        email = dict1.get('email')
        # 验证
        if not all([email]):
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'没有邮箱参数'
            })
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'邮箱格式错误'
            })
        #处理
        #修改属性
        user = request.user
        user.email = email
        user.save()
        #发邮件
        token = meiduo_signature.dumps({'user_id':user.id},contants.EMAIL_EXPIRES)
        verify_url = settings.EMAIL_VERIFY_URL + '?token=%s'% token
        send_user_email.delay(email,verify_url)

        #响应
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK'
        })

class EmailverifyView(View):
    def get(self,request):
        # 接收
        token = request.GET.get('token')
        #验证
        dict1 = meiduo_signature.loads(token,contants.EMAIL_EXPIRES)
        if dict1 is None:
            return http.HttpResponseBadRequest('激活信息无效,请重新发邮件')
        user_id = dict1.get('user_id')

        #处理
        try:
            user = User.objects.get(pk=user_id)
        except:
            return http.HttpResponseBadRequest('激活信息无效')
        else:
            user.email_active = True
            user.save()
        #响应
        return redirect('/info/')

class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        # 查询当前用户的收货地址
        user = request.user
        address_list = Address.objects.filter(user = user,is_delete=False)
        # 将python对象转换成字典,供js使用
        address_list2 = []
        for address in address_list:
            address_list2.append(address.to_dict())
        context = {
            'addresses':address_list2,
            'user':user
        }
        return render(request, 'user_center_site.html',context)

class CreateAddressView(LoginRequiredMixin,View):
    def post(self, request):
        # 判断收获地址数量不超过20个
        count = request.user.addresses.count()
        if count > contants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({
                'code':RETCODE.THROTTLINGERR,
                'errmsg':'收获地址超过20个'
            })
        # 添加收货地址
        user = request.user
        # 接收
        '''
        request.GET===>查询参数
        request.POST===><form method='post'></form>
        request.body===>ajax请求中的json数据
        '''
        dict1 = json.loads(request.body.decode())
        # title = dict1.get('title')
        receiver = dict1.get('receiver')
        province_id = dict1.get('province_id')
        city_id = dict1.get('city_id')
        district_id = dict1.get('district_id')
        place = dict1.get('place')
        mobile = dict1.get('mobile')
        tel = dict1.get('tel')
        email = dict1.get('email')

        # 验证
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '参数不完整'
            })
        # 格式验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '手机号格式错误'
            })
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.JsonResponse({
                    'code': RETCODE.PARAMERR,
                    'errmsg': '固定电话格式错误'
                })
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.JsonResponse({
                    'code': RETCODE.PARAMERR,
                    'errmsg': '邮箱格式错误'
                })

        # 处理：添加，创建对象***.objects.create()
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            detail=place,
            mobile=mobile,
            phone=tel,
            email=email
        )
        # 判断当前用户是否有默认地址，如果没有则设置为当前地址
        if user.default_address is None:
            user.default_address = address
            user.save()

        # 响应
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'ok',
            'address': address.to_dict()
        })

class AddressUpdateView(LoginRequiredMixin,View):
    def put(self,request,address_id):
        #接收
        dict1 = json.loads(request.body.decode())
        # title = dict1.get('title')
        receiver = dict1.get('receiver')
        province_id = dict1.get('province_id')
        city_id = dict1.get('city_id')
        district_id = dict1.get('district_id')
        place = dict1.get('place')
        mobile = dict1.get('mobile')
        tel = dict1.get('tel')
        email = dict1.get('email')
        # 验证
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '参数不完整'
            })
        # 格式验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({
                'code': RETCODE.PARAMERR,
                'errmsg': '手机号格式错误'
            })
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.JsonResponse({
                    'code': RETCODE.PARAMERR,
                    'errmsg': '固定电话格式错误'
                })
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.JsonResponse({
                    'code': RETCODE.PARAMERR,
                    'errmsg': '邮箱格式错误'
                })
        # 处理
        user = request.user
        try:
            address = Address.objects.get(pk = address_id,user=user,is_delete=False)
        except:
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'收货地址编码无效'
            })
        address.receiver = receiver
        address.province_id = province_id
        address.city_id = city_id
        address.district_id = district_id
        address.detail = place
        address.mobile = mobile
        address.phone = tel
        address.email = email
        address.save()

        #响应
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok',
            'address':address.to_dict()
        })
    def delete(self,request,address_id):
        # 查询对象的is_detele,是否为True

        try:
            address = Address.objects.get(pk=address_id,user=request.user,is_delete=False)
        except:
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'收货地址编号无效'
            })
        # 逻辑删除
        address.is_delete = True
        address.save()

        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok'
        })

class AddressDefaultView(LoginRequiredMixin,View):
    def put(self,request,address_id):
        user = request.user
        user.default_address_id = address_id
        user.save()
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok'
        })

class AddressTitleView(LoginRequiredMixin,View):
    def put(self,request,address_id):
        dict1 = json.loads(request.body.decode())
        title = dict1.get('title')

        if not all([title]):
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'收货地址标题不能为空'
            })
        try:
            address = Address.objects.get(pk=address_id,user=request.user,is_delete=False)
        except:
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'收货地址编号无效'
            })
        address.title = title
        address.save()
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok'
        })

class PasswordView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'user_center_pass.html')
    def post(self,request):
        # 接收
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        new_cpwd = request.POST.get('new_cpwd')
        #验证
        if not all([old_pwd,new_pwd,new_cpwd]):
            return http.HttpResponseBadRequest('参数不完整')
        user = request.user
        if not user.check_password(old_pwd):
            return http.HttpResponseBadRequest('原密码错误')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_pwd):
            return http.HttpResponseBadRequest('密码格式错误')
        # 新密码是否一致
        if new_pwd != new_cpwd:
            return http.HttpResponseBadRequest('两次密码不一致')
        # 处理 修改密码
        user.set_password(new_pwd)
        user.save()
        return render(request,'user_center_pass.html')
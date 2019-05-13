from meido_mall.utils.response_code import RETCODE
from django.shortcuts import render,redirect
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django import http
from django.conf import settings
from .models import OAUthQQUser
from django.contrib.auth import login
from meido_mall.utils import meiduo_signature
from . import contants
from users.models import User
from carts.utils import merge_carts_cookie_to_redis

# Create your views here.



class QQurlView(View):
    def get(self,request):
        # 生成QQ的授权url
        next_url = request.GET.get('next','/')
        # 创建工具对象,包括appid,appkey,回调地址
        oauthqq_tool = OAuthQQ(
            settings.QQ_CLIENT_ID,
            settings.QQ_CLIENT_SECRET,
            settings.QQ_REDIRECT_URI,
            next_url
        )
        # 调用方法生成授权地址
        login_url = oauthqq_tool.get_qq_url()
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK',
            'login_url':login_url
        })



class QQopenidView(View):
    def get(self,request):
        # 接收code
        code = request.GET.get('code')
        # 生成QQ的授权url
        next_url = request.GET.get('state', '/')
        # 创建工具对象,包括appid,appkey,回调地址
        oauthqq_tool = OAuthQQ(
            settings.QQ_CLIENT_ID,
            settings.QQ_CLIENT_SECRET,
            settings.QQ_REDIRECT_URI,
            next_url
        )
        try:
            # 接收token
            token = oauthqq_tool.get_access_token(code)
            # 接收openid
            openid = oauthqq_tool.get_open_id(token)
            try:
                #检查是否已经绑定过
                qquser = OAUthQQUser.objects.get(openid = openid)
            except:
                #如果未绑定过,则提示绑定页面
                token = meiduo_signature.dumps({'openid':openid},contants.OPENID_EXPIRES)
                context = {'token':token}
                return render(request, 'oauth_callback.html',context)
            else:
                # 如果绑定过,则状态保持
                login(request,qquser.user)
                response = redirect(next_url)
                response.set_cookie('username',qquser.user.username,max_age=60*60*24*14)
                return response
        except:
            openid = 'code过期'



        return http.HttpResponse(openid)

    def post(self,request):
        #接收
        # openid与帐号绑定
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('pwd')
        sms_code_request = request.POST.get('sms_code')
        access_token = request.POST.get('access_token')
        next_url = request.GET.get('state')
        #验证
        #openid
        json = meiduo_signature.loads(access_token,contants.OPENID_EXPIRES)
        if json is None:
            return http.HttpResponseBadRequest('授权信息无效,请重新授权')
        openid = json.get('openid')
        #处理
        # 根据手机号查询用户对象
        try:
            user = User.objects.get(mobile = mobile)
        except:
            #手机号不存在,则注册新用户
            user = User.objects.create_user(username=mobile,password = pwd,mobile = mobile)
        else:
            #手机号存在,验证密码
            if not user.check_password(pwd):
                return http.HttpResponseBadRequest('密码错误')
        #绑定
        OAUthQQUser.objects.create(openid=openid,user = user)
        # 状态保持
        login(request,user)
        #响应
        response = redirect(next_url)
        response = merge_carts_cookie_to_redis(request,response)
        response.set_cookie('username',user.username,max_age=60*60*24*14)
        return response

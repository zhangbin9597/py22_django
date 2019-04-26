from meido_mall.utils.response_code import RETCODE
from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django import http
from django.conf import settings
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
        except:
            openid = 'code过期'

        return http.HttpResponse(openid)


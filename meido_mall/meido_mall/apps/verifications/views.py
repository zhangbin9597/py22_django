from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meido_mall.libs.captcha.captcha import captcha
from . import contants
# Create your views here.

class ImagecodeView(View):
    def get(self,request,uuid):
        # 接收
        # 验证
        # 处理:
        # 1.生成图形验证码数据：字符code、图片image
        text,code,image = captcha.generate_captcha()

        # 2.保存字符,用于后续验证
        # 2.1 连接redis,参数为caches中的键
        redis_cli = get_redis_connection('verify_code')
        # 2.2 向redis中学术据
        redis_cli.setex(uuid,contants.IMAGE_CODE_EXPIRES,code)
        #响应:输出图片数据
        return http.HttpResponse(image,content_type='image/png')



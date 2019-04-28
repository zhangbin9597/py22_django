import random
from celery_tasks.sms.tasks import send_sms
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meido_mall.libs.captcha.captcha import captcha
from meido_mall.utils.response_code import RETCODE
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

class SmscodeView(View):
    """短信验证"""
    def get(self,request,mobile):
        """

        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        image_code_request = request.GET.get('image_code')#用户填写的图形验证码文本
        uuid = request.GET.get('image_code_id')#图形验证码的唯一编号

        #验证图形验证码是否正确
        redis_cli = get_redis_connection('verify_code')
        image_code_redis = redis_cli.get(uuid)
        #判断是否存在
        if not image_code_redis:
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'图形码已过期'
            })
        #判断用户输入的值是否正确
        #注意1:redis中读取的数据是BYTES类型,需要手动转换成str
        #注意2:忽略大小写
        if image_code_redis.decode() != image_code_request.upper():
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'图形验证码错误'
            })
        #是否已经向此手机号发过短信
        if redis_cli.get('sms_flag_' + mobile):
            return http.JsonResponse({
                'code':RETCODE.PARAMERR,
                'errmsg':'已经向此手机发送过短信,请查看手机'
            })
        #处理
        #1.生成6位随机数
        sms_code = '%06d' % random.randint(0, 999999)
        #2.保存到redis
        # redis_cli.setex('sms_'+mobile,contants.SMS_CODE_EXPIRES,sms_code)
        # 存储60s发送的标记
        # redis_cli.setex('sms_flag_'+ mobile,contants.SMS_CODE_FLAG_EXPIRES,1)
        # 使用pipeline，只与redis服务器交互一次，执行多条命令
        # 创建Redis管道
        redis_pl = redis_cli.pipeline()
        # 将Redis请求添加到队列
        redis_pl.setex('sms_'+mobile,contants.SMS_CODE_EXPIRES,sms_code)
        redis_pl.setex('sms_flag_'+ mobile,contants.SMS_CODE_FLAG_EXPIRES,1)
        # 执行请求
        redis_pl.execute()
        # 3发短信
        # ccp = CCP()
        # ret = ccp.send_template_sms(mobile, [sms_code, contants.SMS_CODE_EXPIRES / 60], 1)
        print(sms_code)
        # send_sms.delay(mobile, [sms_code, contants.SMS_CODE_EXPIRES / 60], 1)

        #响应
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK'
        })





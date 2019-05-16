from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from alipay import AliPay
from orders.models import OrderInfo
from django import http
from meido_mall.utils.response_code import RETCODE
from django.conf import settings
import os
from .models import Payment

class PaymentView(LoginRequiredMixin, View):
    """订单支付功能"""

    def get(self,request, order_id):
        pass
        try:
            order = OrderInfo.objects.get(pk=order_id)
        except:
            return http.JsonResponse({'code':RETCODE.PARAMERR,'errmsg':'订单编号无效'})

        #调用支付宝的接口,生成地址
        #1.创建支付宝对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 支付宝应用标识
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/alipay/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/alipay/app_public_key.pem'),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        # 2.生成参数
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='美多商城',
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        #3 拼接链接
        alipay_url = settings.ALIPAY_URL + "?" + order_string

        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': '',
            'alipay_url': alipay_url
        })

class AlipayVerifyView(View):
    def get(self,request):
        param_dict = request.GET.dict()  # QueryDict===>dict(){}
        # print(param_dict)
        '''
        {
            'out_trade_no': '20190515105744000000001', #订单编号
            'app_id': '2016082100304973',
            'trade_no': '2019051622001420411000006668', #支付宝生成的流水号
            'charset': 'utf-8',
            'auth_app_id': '2016082100304973',
            'timestamp': '2019-05-16 09:07:51',
            'version': '1.0',
            'method': 'alipay.trade.page.pay.return',
            'sign_type': 'RSA2',
            'seller_id': '2088102172415825',
            'total_amount': '3388.00',
            'sign': 'dYq2FyMx7h+UTi8wIe3ng1URK51kyHYGPQqV2lm9BFg8ZukYpVuAFIJCcamdN8STQDmUUUppUQapiFC9tdwei2LoEMp2PyAo/OFQh7C87g+Jp6H8PO0Rlq5rhWKMdcuqb8W73d8WmvkUxlAzipIb6Yk5Geo5sj4B5Ji1IvZ+fEioch/JnxCL6XzH/1D10K7rSmmZPtktYv80r6UhZFzR42omzi8JZyY++MbiyVxm9mKeJdnvoatTU7MZPHWwRz/+KLlEHJhLS5m/90g8QLfH6QASqLFeA0LJSFDqsVWuRuMVP2wlCA+Os3JV7Mw8QTHLLB7hWUPbT0BF9xpseN3K0A=='
        }
        '''
        signature = param_dict.pop("sign")
        # 创建支付宝对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 支付宝应用标识
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/alipay/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/alipay/app_public_key.pem'),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 验证是否支付成功
        result = alipay.verify(param_dict, signature)
        # print(result)
        if result:
            # 支付成功
            # 1.保存支付宝流水号
            alipay_id = param_dict.get('trade_no')
            Payment.objects.create(
                order_id=param_dict.get('out_trade_no'),
                trade_id=alipay_id
            )
            # 2.修改订单的状态为待发货-2
            OrderInfo.objects.filter(pk=param_dict.get('out_trade_no')).update(status=2)

            context = {
                'alipay_id': alipay_id
            }
            return render(request, 'pay_success.html', context)
        else:
            # 支付失败
            return http.HttpResponse('支付失败，请到我的订单中重新支付')




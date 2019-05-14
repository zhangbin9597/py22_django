from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Address
from goods.models import SKU
from django_redis import get_redis_connection
import json
from django import http
from meido_mall.utils.response_code import RETCODE
from datetime import datetime
from .models import OrderInfo, OrderGoods
from django.db import transaction
from django.core.paginator import Paginator


# Create your views here.

class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        user = request.user
        # 查询收货地址
        addresses = Address.objects.filter(is_delete=False, user_id=user.id)
        default_address_id = user.default_address_id
        # 查询购物车中选中的商品，当前视图需要登录后才能访问，只通过redis获取购物车数据
        redis_cli = get_redis_connection('carts')
        # hash
        cart_dict = redis_cli.hgetall('cart%d' % user.id)
        cart_dict = {int(sku_id): int(count) for sku_id, count in cart_dict.items()}
        # set
        selected_list = redis_cli.smembers('selected%d' % user.id)
        selected_list = [int(sku_id) for sku_id in selected_list]
        # 查询库存商品对象
        skus = SKU.objects.filter(pk__in=selected_list, is_launched=True)
        # 转换为前端需要的格式
        sku_list = []
        total_count = 0
        total_money = 0
        freight = 10  # 运费，在实际工作中按照合作快递公司的标准计算
        for sku in skus:
            # 总数量
            total_count += cart_dict[sku.id]
            # 小计
            total_amount = sku.price * cart_dict[sku.id]
            # 总计
            total_money += total_amount
            sku_list.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price,
                'count': cart_dict[sku.id],
                'total_amount': total_amount
            })
        pay_money = total_money + freight

        context = {
            'addresses': addresses,
            'default_address_id': default_address_id,
            'sku_list': sku_list,
            'total_count': total_count,
            'total_money': total_money,
            'freight': freight,
            'pay_money': pay_money
        }
        return render(request, 'place_order.html', context)


class OrderCommitView(LoginRequiredMixin, View):
    def post(self, request):
        '''
        创建订单对象、订单商品对象
        参数 address_id：收货地址编号
        参数 pay_method：支付方式编号
        '''
        user = request.user
        # 接收
        param_dict = json.loads(request.body.decode())
        address_id = param_dict.get('address_id')
        pay_method = param_dict.get('pay_method')

        # 验证
        if not all([address_id, pay_method]):
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '参数不完整'})
        # 收货地址有效性
        try:
            address = Address.objects.get(pk=address_id, user_id=user.id)
        except:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '收货地址无效'})
        # 支付方式，当前只允许[1,2]
        if pay_method not in [1, 2]:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '支付方式无效'})

        # 1.从购物车中查询选中的商品
        redis_cli = get_redis_connection('carts')
        cart_dict = redis_cli.hgetall('cart%d' % user.id)
        cart_dict = {int(sku_id): int(count) for sku_id, count in cart_dict.items()}
        selected_list = redis_cli.smembers('selected%d' % user.id)
        selected_list = [int(sku_id) for sku_id in selected_list]

        # 创建事务
        with transaction.atomic():
            # 开启事务
            sid = transaction.savepoint()
            # 2.创建订单对象
            now = datetime.now()
            total_count = 0
            total_amount = 0
            if pay_method == 1:  # 货到付款
                status = 2
            else:
                status = 1
            order_id = '%s%09d' % (now.strftime('%Y%m%d%H%M%S'), user.id)
            order = OrderInfo.objects.create(
                order_id=order_id,
                user_id=user.id,
                address_id=address_id,
                total_count=total_count,
                total_amount=total_amount,
                freight=10,
                pay_method=pay_method,
                status=status
            )
            # 3.查询库存商品，遍历
            skus = SKU.objects.filter(pk__in=selected_list, is_launched=True)
            for sku in skus:
                count = cart_dict[sku.id]
                # 3.1判断库存是否足够，如果不足则返回提示，如果库存足够，则继续
                if sku.stock < count:
                    transaction.savepoint_rollback(sid)
                    return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                # 3.2修改商品的库存、销量
                # sku.stock -= count
                # sku.sales += count
                # sku.save()
                stock_old = sku.stock
                stock_new = sku.stock - count
                sales_new = sku.sales + count
                result = SKU.objects.filter(pk=sku.id, stock=stock_old).update(stock=stock_new, sales=sales_new)
                # result表示修改的行数
                if result == 0:
                    # 回滚事务
                    transaction.savepoint_rollback(sid)
                    return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '服务器繁忙,请稍候再试'})
                # 3.3创建订单商品对象
                order_goods = OrderGoods.objects.create(
                    order_id=order_id,
                    sku_id=sku.id,
                    count=count,
                    price=sku.price
                )
                # 3.4计算总数量、总金额
                total_count += count
                total_amount += count * sku.price
            # 4.修改订单对象的总金额、总数量
            order.total_count = total_count
            order.total_amount = total_amount
            order.save()
            transaction.savepoint_commit(sid)
        # 5.删除购物车中选中的商品
        redis_cli.hdel('cart%d' % user.id, *selected_list)
        redis_cli.delete('selected%d' % user.id)

        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'ok',
            'order_id': order_id
        })


class SuccessView(LoginRequiredMixin, View):
    def get(self, request):
        # 接收数据
        param_dict = request.GET
        #order_id=20190514084957000000013&payment_amount=22738&pay_method=2
        order_id = param_dict.get('order_id')
        payment_amount = param_dict.get('payment_amount')
        pay_method = param_dict.get('pay_method')

        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context)

class OrderInfoView(LoginRequiredMixin,View):
    def get(self, request, page_num):
        # 查询当前用户的所有订单
        order_list = OrderInfo.objects.filter(user_id=request.user.id).order_by('-create_time')

        # 分页
        paginator = Paginator(order_list, 2)
        page = paginator.page(page_num)

        # 转换成前端需要的格式
        page_list = []
        for order in page:
            detail_list = []
            for detail in order.skus.all():
                detail_list.append({
                    'default_image_url': detail.sku.default_image.url,
                    'name': detail.sku.name,
                    'price': detail.price,
                    'count': detail.count,
                    'total': detail.price * detail.count
                })

            page_list.append({
                'create_time': order.create_time,
                'order_id': order.order_id,
                'detail_list': detail_list,
                'total_amount': order.total_amount,
                'freight': order.freight,
                'status': order.status,
            })

        context = {
            'page': page_list,
            'page_num': page_num,
            'page_total': paginator.num_pages
        }

        return render(request, 'user_center_order.html', context)

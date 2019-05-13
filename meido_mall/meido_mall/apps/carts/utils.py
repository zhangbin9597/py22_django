from meiduo_mall.utils import meiduo_json
from django_redis import get_redis_connection


def merge_carts_cookie_to_redis(request, response):
    '''
    将cookie中的购物车数据转存到redis中
    :param request: 请求对象
    :param response: 响应对象
    :return: 响应对象
    以cookie中的数据覆盖redis中的数据
    '''
    user = request.user
    # 1.读取cookie中购物车数据
    cart_str = request.COOKIES.get('cart')
    if cart_str is None:
        return response
    cart_dict = meiduo_json.loads(cart_str)
    # 2.遍历，保存到redis中
    redis_cli = get_redis_connection('carts')
    redis_pl = redis_cli.pipeline()
    for sku_id, cart in cart_dict.items():
        # 向hash中添加数据
        redis_pl.hset('cart%d' % user.id, sku_id, cart['count'])
        # 如果选中则向set中添加，如果不选中则删除set中的库存商品编号
        if cart['selected']:
            redis_pl.sadd('selected%d' % user.id, sku_id)
        else:
            redis_pl.srem('selected%d' % user.id, sku_id)
    redis_pl.execute()
    # 3.删除cookie中购物车数据
    response.delete_cookie('cart')
    return response

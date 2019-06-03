from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical, users, specs, images, skus, orders, permission, groups, admins, spus, options, brands, \
    channels
from rest_framework.routers import DefaultRouter, SimpleRouter

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^statistical/total_count/$', statistical.UserTotalCount.as_view()),
    url(r'^statistical/day_increment/$', statistical.DayCreateCount.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveCountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # user
    url(r'^users/$', users.UservisitView.as_view()),
    # spec
    url(r'^goods/simple/$', specs.SPUSpecView.as_view({'get': 'simple'})),
    # 图片
    url(r'^skus/simple/$', images.ImageView.as_view({'get': 'simple'})),
    # sku
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SKUView.as_view({'get': 'specs'})),
    # 权限列表
    url(r'^permission/content_types/$', permission.PermissionView.as_view({'get': 'content_types'})),
    # 用户组
    url(r'^permission/simple/$', groups.GroupView.as_view({'get': 'simple'})),
    # admin
    url(r'^permission/groups/simple/$', admins.AdminView.as_view({'get': 'simple'})),
    # spu
    url(r'^goods/brands/simple/$', spus.SPUView.as_view({'get': 'simple'})),
    url(r'^goods/channel/categories/$', spus.SPUView.as_view({'get': 'categorie'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.SPUView.as_view({'get': 'categories'})),
    # specsoption
    url(r'^goods/specs/simple/$', options.OptionView.as_view({'get': 'simple'})),
    # channel
    url(r'^goods/channel_types/$', channels.ChannelView.as_view({'get': 'channel_types'})),
    url(r'^goods/categories/$', channels.ChannelView.as_view({'get': 'categories'})),
]
# 商品
routers = DefaultRouter()
routers.register('goods/specs', specs.SPUSpecView, base_name='specs')
urlpatterns += routers.urls
# 图片管理
routers = DefaultRouter()
routers.register('skus/images', images.ImageView, base_name='images')
urlpatterns += routers.urls
# 图片管理
routers = DefaultRouter()
routers.register('skus', skus.SKUView, base_name='skus')
urlpatterns += routers.urls
# 订单管理
routers = DefaultRouter()
routers.register('orders', orders.OrderView, base_name='orders')
urlpatterns += routers.urls

# 权限管理
routers = DefaultRouter()
routers.register('permission/perms', permission.PermissionView, base_name='perms')
urlpatterns += routers.urls
# 用户组管理
routers = DefaultRouter()
routers.register('permission/groups', groups.GroupView, base_name='groups')
urlpatterns += routers.urls
# 用户组管理
routers = DefaultRouter()
routers.register('permission/admins', admins.AdminView, base_name='admins')
urlpatterns += routers.urls
# brand
routers = DefaultRouter()
routers.register('goods/brands', brands.BrandView, base_name='brands')
urlpatterns += routers.urls
# channel
routers = DefaultRouter()
routers.register('goods/channels', channels.ChannelView, base_name='channels')
urlpatterns += routers.urls
# SPU
routers = DefaultRouter()
routers.register('goods', spus.SPUView, base_name='spus')
urlpatterns += routers.urls
# Option
routers = DefaultRouter()
routers.register('specs/options', options.OptionView, base_name='options')
urlpatterns += routers.urls


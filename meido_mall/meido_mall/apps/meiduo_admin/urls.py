from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical,users,specs,images,skus
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^statistical/total_count/$', statistical.UserTotalCount.as_view()),
    url(r'^statistical/day_increment/$', statistical.DayCreateCount.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveCountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    #user
    url(r'^users/$',users.UservisitView.as_view()),
    #spec
    url(r'^goods/simple/$',specs.SPUSpecView.as_view({'get':'simple'})),
    #图片
    url(r'^skus/simple/$',images.ImageView.as_view({'get':'simple'})),
    #sku
    url(r'^goods/(?P<pk>\d+)/specs/$',skus.SKUView.as_view({'get':'specs'})),
]
#商品
routers = DefaultRouter()
routers.register('goods/specs',specs.SPUSpecView,base_name='specs')
urlpatterns += routers.urls
#图片管理
routers = DefaultRouter()
routers.register('skus/images',images.ImageView,base_name='images')
urlpatterns += routers.urls
#图片管理
routers = DefaultRouter()
routers.register('skus',skus.SKUView,base_name='skus')
urlpatterns += routers.urls

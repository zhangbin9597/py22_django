from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical,users,specs
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

]

routers = DefaultRouter()
routers.register('goods/specs',specs.SPUSpecView,base_name='specs')
urlpatterns += routers.urls
# routers1 = DefaultRouter()
# routers1.register('goods/simple',specs.SPUSpecView,base_name='simple')
# urlpatterns += routers1.urls

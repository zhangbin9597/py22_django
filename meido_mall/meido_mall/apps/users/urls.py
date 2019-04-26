from django.conf.urls import url
from . import views
# from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^register/$', views.register.as_view()),
    url('^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    url('^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$',views.LoginView.as_view()),
    url(r'^logout/$',views.LogoutView.as_view()),
    #验证是否登录的装饰器
    # url(r'^info/$',login_required(views.UserInfoView.as_view())),
    url(r'^info/$',views.UserInfoView.as_view()),
]
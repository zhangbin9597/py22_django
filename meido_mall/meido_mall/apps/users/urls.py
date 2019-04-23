from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register.as_view()),
    url('^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    url('^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # url(r'', views.IndexView.as_view(), name='index'),
]
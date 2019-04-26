from django.conf.urls import url
from . import views
urlpatterns=[
    url('^image_codes/(?P<uuid>[\w-]+)/$', views.ImagecodeView.as_view()),
    url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmscodeView.as_view()),
]
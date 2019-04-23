from django.conf.urls import url
from . import views
urlpatterns=[
    url('^image_codes/(?P<uuid>[\w-]+)/$', views.ImagecodeView.as_view()),
]
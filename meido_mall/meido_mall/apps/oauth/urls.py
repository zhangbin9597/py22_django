from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^qq/login/$',views.QQurlView.as_view()),
    url(r'^oauth_callback$',views.QQopenidView.as_view()),
]


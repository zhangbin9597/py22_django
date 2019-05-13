from django.conf.urls import url
from . import views

urlpatterns = [
    url('^carts/$', views.CartView.as_view()),
    url('^carts/selection/$', views.CartSelectView.as_view()),
    url('^carts/simple/$', views.CartSimpleView.as_view()),
]

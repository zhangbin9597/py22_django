from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),
    url(r'^orders/success/$', views.SuccessView.as_view()),
    url(r'^orders/info/(?P<page_num>\d+)$', views.OrderInfoView.as_view()),
    url(r'^orders/comment/$', views.CommentVIew.as_view()),
    url(r'^comment/(?P<sku_id>\d+)/$', views.CommentListView.as_view()),
]

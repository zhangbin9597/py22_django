from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'list/(?P<category_id>\d+)/(?P<page_num>\d+)/',views.ListView.as_view()),
    url(r'^hot/(?P<category_id>\d+)/$',views.HotView.as_view()),
    url(r'^detail/(?P<sku_id>\d+)/$',views.DetailView.as_view()),
<<<<<<< HEAD
    url(r'^detail/visit/(?P<category_id>\d+)/$',views.DetailVisitView.as_view()),
    url(r'^browse_histories/$',views.HistoryView.as_view()),
=======
>>>>>>> 6488497d5a2fb2670b8a2f99d02f4a0d40424eb9
]
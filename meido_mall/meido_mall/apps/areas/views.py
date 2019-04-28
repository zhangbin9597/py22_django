from django.shortcuts import render

# Create your views here.
from django.views import View


class AreaView(View):
    def get(self,request):

        #接收
        area_id = request.GET.get('area_id')

        # 验证

        # 处理

        #响应

from django.shortcuts import render
from goods.models import GoodsChannel,GoodsCategory
# Create your views here.
from django.views import View
from meido_mall.utils.meido_category import get_category
from contents.models import ContentCategory,Content


class IndexView(View):
    # 首页广告
    def get(self,request):
        """提供首页广告页面"""
        #1.查询频道分类信息
        categories = get_category()

        #2.查询广告信息
        contents = ContentCategory.objects.all()
        contents_dict = {}
        for content in contents:
            contents_dict[content.key] = content.content_set.filter(status=True).order_by('sequence')
        #渲染上下文
        context={
            'categories':categories,
            'contents':contents_dict
        }
        return render(request,'index.html',context)
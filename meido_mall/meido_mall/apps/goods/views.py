from django.shortcuts import render
from django.views import View
# Create your views here.
from meido_mall.utils.meido_category import get_category
from .models import GoodsCategory,SKU
from django.core.paginator import Paginator
from . import constants
from django import http
from meido_mall.utils.response_code import RETCODE

class ListView(View):
    def get(self,request,category_id,page_num):
        # 查询第三级分类对象
        try:
            category3 = GoodsCategory.objects.get(pk=category_id)
        except:
            return render(request,'404.html')

        #分类数据
        categories = get_category()

        #面包屑导航
        category2 = category3.parent
        category1 = category2.parent

        breadcrumb = {
            'cat1':{
                'name':category1.name,
                'url':category1.goodschannel_set.all()[0].url
            },
            'cat2':category2,
            'cat3':category3
        }
        #当前分类数据
        skus = category3.sku_set.filter(is_launched=True)

        #排序
        sort = request.GET.get('sort','default')
        if sort == 'hot':
            skus = skus.order_by('-sales')
        elif sort == 'price':
            skus = skus.order_by('price')
        else:
            skus = skus.order_by('-id')

        # 分页
        # 创建分页对象
        paginator = Paginator(skus,constants.LIST_PER_PAGE)
        # 获取指定页的数据
        page_skus = paginator.page(page_num)
        context={
            'categories':categories,
            'breadcrumb':breadcrumb,
            'page_skus':page_skus,
            'category':category3,
            'sort':sort,
            'page_num':page_num,
            'total_page':paginator.num_pages
        }
        return render(request,'list.html',context)

class HotView(View):
    def get(self,request,category_id):
        #查询2个最热销的商品
        skus = SKU.objects.filter(is_launched=True,category_id=category_id).order_by('-sales')[0:2]

        #格式转换
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'default_image_url':sku.default_image.url,
                'price':sku.price
            })

        #响应
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'ok',
            'hot_sku_list':sku_list
        })


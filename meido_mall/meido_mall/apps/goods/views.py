from django.shortcuts import render
from django.views import View
# Create your views here.
from meido_mall.utils.meido_category import get_category
from .models import GoodsCategory,SKU
from django.core.paginator import Paginator
from . import constants
from django import http
from meido_mall.utils.response_code import RETCODE
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from meido_mall.utils.breadcrumb import get_breadcrumb

class ListView(LoginRequiredMixin,View):
    def get(self,request,category_id,page_num):
        # 查询第三级分类对象
        try:
            category3 = GoodsCategory.objects.get(pk=category_id)
        except:
            return render(request,'404.html')

        #分类数据
        categories = get_category()

        #面包屑导航
        breadcrumb = get_breadcrumb(category3)
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
        #状态保持
        user = request.user
        login(request,user)
        context={
            'username':user.username,
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

class DetailView(View):
    def get(self,request,sku_id):
        # 获取当前sku的信息
        try:
            sku = SKU.objects.get(pk=sku_id)
        except:
            return render(request,'404.html')
        category3 = sku.category
        # 查询商品频道分类
        categories = get_category()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category3)
        # sku对象数据：在前面已经根据编号查询
        # 当前库存商品的规格选项信息，结果如编号为16的库存商品对应的选项为
        sku_option = sku.specs.order_by('spec_id')
        sku_option_list = [info.option_id for info in sku_option]
        # 标准商品spu
        spu = sku.spu
        # 标准商品===》所有库存商品===》所有选项信息
        skus = spu.sku_set.filter(is_launched=True)
        sku_option_dict = {}
        for sku_info in skus:
            # 获取9号商品的库存列表为[13,20],10号商品库存为[13,21],.....
            sku_info_option = sku_info.specs.order_by('spec_id')
            sku_info_option_list = [option_info.option_id for option_info in sku_info_option]
            sku_option_dict[tuple(sku_info_option_list)]=sku_info.id
        """
            (13,20):9
            (13,21):10
            .....
        """
        # print(sku_option_dict)
        # sku==>spu==>规格===>选项
        specs = spu.specs.all()
        specs_list=[]
        for index,spec in enumerate(specs):
            # 转换规格数据
            spec_dict = {
                'name': spec.name,
                'options':[]
            }
            # 查询规格的选项
            options = spec.options.all()
            for option in options:
                option_dict={
                    'name': option.value,
                    'id':option.id,
                }
                #复制当前库存商品的选项
                sku_option_list_temp = sku_option_list[:]
                # 当前选项是否选中
                if option.id in sku_option_list:
                    option_dict['selected'] = True
                else:
                    option_dict['selected'] = False
                # 为选项指定库存商品编号
                sku_option_list_temp[index] = option.id
                # print(sku_option_list_temp[index])
                option_dict['sku_id'] = sku_option_dict[tuple(sku_option_list_temp)]
                # print(sku_option_dict[tuple(sku_option_list_temp)])
                # 输出的是sku中的id 所有选中的sku.name
                spec_dict['options'].append(option_dict)
            # 添加规格数据
            specs_list.append(spec_dict)



        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
            'spu':spu,
            'category_id':category3.id,
            'specs':specs_list,
        }
        return render(request,'detail.html',context)

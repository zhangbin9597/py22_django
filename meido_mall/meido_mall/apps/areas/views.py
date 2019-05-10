from django import http
from django.core.cache import cache

from meido_mall.utils.response_code import RETCODE
from django.shortcuts import render
# from django_redis.cache import logger
from . import contants
from .models import Area
# Create your views here.
from django.views import View


class AreaView(View):
    def get(self,request):

        #接收
        area_id = request.GET.get('area_id')

        # 验证
        if not area_id:
            # 读取省份缓存数据
            province_list = cache.get('province_list')
            # 提供省份数据
            if not province_list:
                try:
                    # 查询省份数据
                    provinces = Area.objects.filter(parent__isnull=True)

                    # 序列化省级数据
                    province_list = []
                    for province in provinces:
                        province_list.append({
                            'id': province.id,
                            'name': province.name
                        })
                except Exception as e:
                    # logger.error(e)
                    return http.JsonResponse({
                        'code': RETCODE.DBERR,
                        'errmsg': '省份数据错误'
                    })
                # 缓存
                cache.set('province_list',province_list,contants.AREA_CACHE_EXPIRES)
            # 响应省份数据
            return http.JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'province_list': province_list
            })


        else:
            # 读取市或区缓存数据
            sub_data = cache.get('area_'+area_id)
            if not sub_data:
                try:
                    #查询市或区的 # 查询指定地区对象，并获取子级地址
                    area = Area.objects.get(pk = area_id)
                except:
                    return http.JsonResponse({
                        'code':RETCODE.PARAMERR,
                        'errmsg':'无效的地区编号'
                    })
                # 查询子地区
                subs = area.subs.all()
                # 转换成json的格式
                subs_list = []
                for sub in subs:
                    subs_list.append({
                        'id':sub.id,
                        'name':sub.name
                    })
                # 缓存
                sub_data = {
                    'id': area.id,
                    'name': area.name,
                    'subs': subs_list
                }
                cache.set('area_'+area_id,sub_data,contants.AREA_CACHE_EXPIRES)
            return http.JsonResponse({
                'code':RETCODE.OK,
                'errmsg':'OK',
                'sub_data':sub_data
            })


        # 处理

        #响应

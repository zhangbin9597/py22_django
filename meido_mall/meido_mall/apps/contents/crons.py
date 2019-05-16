from django.shortcuts import render
from meido_mall.utils.meido_category import get_category
from contents.models import ContentCategory
import os
from django.conf import settings

def generate_static_index_html():
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
    #获取html字符串
    response = render(None,'index.html',context)
    html_str = response.content.decode()
    #将字符串写入文件中
    file_path = os.path.join(settings.BASE_DIR,'static/index.html')
    with open(file_path,'w') as f1:
        f1.write(html_str)



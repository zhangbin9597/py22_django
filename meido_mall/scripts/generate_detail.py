#!/usr/bin/env python
#!/home/python/.virtualenvs/py3_django/bin/python

import os
import sys

sys.path.insert(0, '../')
# 引入django配置，并启用
os.environ["DJANGO_SETTINGS_MODULE"] = "meido_mall.settings.dev"
import django

django.setup()

from celery_tasks.detail.tasks import generate_static_detail_html
from goods.models import SKU

if __name__ == '__main__':
    '''
    遍历商品表中的数据，生成静态页面
    '''
    skus = SKU.objects.filter(is_launched=True)
    for sku in skus:
        # print('---%d' % sku.id)
        generate_static_detail_html(sku.id)

    print('ok')
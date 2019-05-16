from django.shortcuts import render
from meido_mall.utils.meido_category import get_category
from meido_mall.utils.breadcrumb import get_breadcrumb
from goods.models import SKU
from django.conf import settings
import os
from celery_tasks.main import app


@app.task(name='generate_static_detail_html')
def generate_static_detail_html(sku_id):
    # 获取当前sku的信息
    try:
        sku = SKU.objects.get(pk=sku_id)
    except:
        return render(None, '404.html')
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
        sku_option_dict[tuple(sku_info_option_list)] = sku_info.id
    """
        (13,20):9
        (13,21):10
        .....
    """
    # print(sku_option_dict)
    # sku==>spu==>规格===>选项
    specs = spu.specs.all()

    specs_list = []
    for index, spec in enumerate(specs):
        # 转换规格数据
        spec_dict = {
            'name': spec.name,
            'options': []
        }
        # 查询规格的选项
        options = spec.options.all()
        for option in options:
            option_dict = {
                'name': option.value,
                'id': option.id,
            }
            # 复制当前库存商品的选项
            sku_option_list_temp = sku_option_list[:]

            # 当前选项是否选中
            if option.id in sku_option_list:
                option_dict['selected'] = True
            else:
                option_dict['selected'] = False
            # 为选项指定库存商品编号
            sku_option_list_temp[index] = option.id
            option_dict['sku_id'] = sku_option_dict.get((tuple(sku_option_list_temp)), 0)
            # 输出的是sku中的id 所有选中的sku.name
            spec_dict['options'].append(option_dict)
        # 添加规格数据
        specs_list.append(spec_dict)

    # 渲染页面
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'spu': spu,
        'category_id': category3.id,
        'specs': specs_list,
    }
    response = render(None, 'detail.html', context)
    html_str = response.content.decode()
    file_path = os.path.join(settings.BASE_DIR, 'static/details/%d.html' % sku.id)
    print(file_path)
    with open(file_path, 'w') as f1:
        f1.write(html_str)




from goods.models import GoodsChannel,GoodsCategory
def get_category():
    # 查询商品频道与分类信息
    # 1.1查询所有频道并排序
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 1.2遍历,转换频道结构
    categories = {}
    for channel in channels:
        # 1.3判断此频道是否已经存在,如果不存在则新建字典
        # group_id = channel.group_id
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels': [],
                'sub_cats': []
            }
        # 1.4 获取当前频道
        channel_dict = categories[channel.group_id]
        # 1.5向一级分类中添加数据
        channel_dict['channels'].append({
            'name': channel.category.name,
            'url': channel.url
        })
        # 1.6向二级分类中添加数据
        for cat2 in channel.category.subs.all():
            channel_dict['sub_cats'].append({
                'name': cat2.name,
                # 1.7添加三级分类
                'sub_cats': cat2.subs.all()
            })
    return categories
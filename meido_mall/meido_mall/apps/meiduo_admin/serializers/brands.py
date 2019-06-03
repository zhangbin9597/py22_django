from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.response import Response

from goods.models import Brand
from rest_framework import serializers


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


    def create(self, validated_data):
        #self获取视图的序列化器传递的request
        # 3.保存图片
        # 4.创建fdfs客户端
        c = Fdfs_client(settings.FASTDFS_PATH)
        # 5.读取图片文件数据
        file = self.context['request'].FILES.get('logo')
        # 6.上传图片
        image = c.upload_by_buffer(file.read())
        # 7.判断是否成功
        if image['Status'] != 'Upload successed.':
            return Response({'error': '上传失败'}, status=400)
        img = Brand.objects.create(name=validated_data['name'],first_letter=validated_data['first_letter'],
                                      logo=image['Remote file_id'])
        # 生成详情页静态化
        # generate_static_detail_html.delay(img.sku_id)
        return img

from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage,SKU
from meiduo_admin.serializers.images import ImageSerializer,SKUSerializer
from meiduo_admin.utils import PaginationNum
from rest_framework.response import Response
from rest_framework import serializers
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from django.conf import settings


class ImageView(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = SKUImage.objects.all()
    pagination_class = PaginationNum
    # 指定权限
    permission_classes = [IsAdminUser]
    def simple(self,request):
        data = SKU.objects.all()
        ser = SKUSerializer(data,many=True)
        return Response(ser.data)

    def create(self, request, *args, **kwargs):
        #1.获取前端传来的值
        data = request.data
        #2.验证数据
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        #8.返回图片链接
        # url = settings.FDFS_URL+image['Remote file_id']

        return Response(ser.data)
    def update(self, request, *args, **kwargs):
        # 1.获取前端传来的值
        data = request.data
        #获取对象
        image = self.get_object()
        # 2.验证数据
        ser = self.get_serializer(image, data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        # 8.返回图片链接
        # url = settings.FDFS_URL+image['Remote file_id']
        return Response(ser.data)

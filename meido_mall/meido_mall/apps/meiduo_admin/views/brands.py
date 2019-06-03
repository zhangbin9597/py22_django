from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.brands import BrandSerializer
from meiduo_admin.utils import PaginationNum
from goods.models import Brand
from django.conf import settings

class BrandView(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def create(self, request, *args, **kwargs):
        # 1.获取前端传来的值
        data = request.data
        # 2.验证数据
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        # 8.返回图片链接
        # url = settings.FDFS_URL+image['Remote file_id']

        return Response(ser.data)
from meiduo_admin.serializers.spus import SPUSerializer,BrandSerializer,GoodsCategorySerializer
from goods.models import SPU,GoodsCategory,Brand
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PaginationNum


class SPUView(ModelViewSet):
    serializer_class = SPUSerializer
    queryset = SPU.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def simple(self,request):
        data = Brand.objects.all()
        ser = BrandSerializer(data,many=True)
        return Response(ser.data)

    def categorie(self,request):
        data = GoodsCategory.objects.filter(parent=None)
        ser = GoodsCategorySerializer(data, many=True)
        return Response(ser.data)
    def categories(self,request,pk):
        data = GoodsCategory.objects.filter(parent_id=pk)
        ser = GoodsCategorySerializer(data, many=True)
        return Response(ser.data)

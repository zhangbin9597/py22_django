from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SKU,GoodsCategory,SPU,SPUSpecification
from meiduo_admin.utils import PaginationNum
from meiduo_admin.serializers.skus import SKUSerializer,GoodcategorySerializer,\
    SPUSpecificationSerializer
from rest_framework.permissions import IsAdminUser

class SKUView(ModelViewSet):
    serializer_class = SKUSerializer
    queryset = SKU.objects.all()
    pagination_class = PaginationNum
    permission_classes = [IsAdminUser]
    #重写get_queryset
    def get_queryset(self):
        # 获取前端传来的数据
        user = self.request.query_params.get('keyword')
        if user == '':
            return SKU.objects.all()
        elif user is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name__icontains=user)
    @action(methods=['get'],detail=False)
    def categories(self,request):
        """获取三级分类"""
        #1.查询三级分类
        data =GoodsCategory.objects.filter(subs__id=None)
        #2.返回分类信息
        ser = GoodcategorySerializer(data,many=True)
        return Response(ser.data)
    def specs(self,request,pk):
        """查询spu对应的规格信息"""
        #1.获取spu商品对象
        spu = SPU.objects.get(id=pk)
        #2.根据spu查询商品对应的规格
        data = spu.specs.all()
        #3.序列化返回
        ser = SPUSpecificationSerializer(data,many=True)
        return Response(ser.data)


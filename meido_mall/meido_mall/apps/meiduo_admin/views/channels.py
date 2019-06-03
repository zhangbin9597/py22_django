from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.channels import ChannelSerializer,GoodsCategorySerializer,GoodGroupSerializer
from meiduo_admin.utils import PaginationNum
from goods.models import GoodsChannel,GoodsChannelGroup,GoodsCategory


class ChannelView(ModelViewSet):
    serializer_class = ChannelSerializer
    queryset = GoodsChannel.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def categories(self,request):
        data = GoodsCategory.objects.all()
        ser = GoodsCategorySerializer(data,many=True)
        return Response(ser.data)
    def channel_types(self,request):
        data = GoodsChannelGroup.objects.all()
        ser = GoodGroupSerializer(data, many=True)
        return Response(ser.data)




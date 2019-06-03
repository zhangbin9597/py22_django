from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from meiduo_admin.utils import PaginationNum
from orders.models import OrderInfo
from meiduo_admin.serializers.orders import OrderSerializer


class OrderView(ModelViewSet):

    serializer_class = OrderSerializer
    queryset = OrderInfo.objects.all()
    pagination_class = PaginationNum
    permission_classes = [IsAdminUser]

    # 重写get_queryset
    def get_queryset(self):
        # 获取前端传来的数据
        user = self.request.query_params.get('keyword')
        if user == '':
            return OrderInfo.objects.all()
        elif user is None:
            return OrderInfo.objects.all()
        else:
            return OrderInfo.objects.filter(order_id__icontains=user)
    @action(methods=['put'],detail=True)
    def status(self,request,pk):
        """修改订单状态"""
        try:
            order = OrderInfo.objects.get(order_id=pk)
        except:
            return Response({'error':'订单号无效'})
        #获取前端传来的订单状态
        status = request.data.get('status')
        if status is None:
            return Response({'error': '状态码无效'})
        order.status = status
        order.save()
        return Response({
            'order_id':pk,
            'status':status
        })
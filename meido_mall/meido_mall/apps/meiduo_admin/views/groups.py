from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group,Permission
from rest_framework.permissions import IsAdminUser
from meiduo_admin.utils import PaginationNum
from meiduo_admin.serializers.groups import GroupSerializer
from meiduo_admin.serializers.permission import PermissionSerializer


class GroupView(ModelViewSet):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def simple(self,request):
        # 1、查询所有权限
        data = Permission.objects.all()
        # 2、返回权限内容
        ser = PermissionSerializer(data, many=True)
        return Response(ser.data)

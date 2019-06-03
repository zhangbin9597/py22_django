from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Permission,ContentType
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.permission import PermissionSerializer,ContntTypeSerializer
from meiduo_admin.utils import PaginationNum


class PermissionView(ModelViewSet):

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def content_types(self,request):
        """添加权限列表"""
        data = ContentType.objects.all()
        ser = ContntTypeSerializer(data,many=True)
        return Response(ser.data)
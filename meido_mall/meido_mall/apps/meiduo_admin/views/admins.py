from rest_framework.response import Response
from users.models import User
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PaginationNum
from meiduo_admin.serializers.admins import AdminSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group
from meiduo_admin.serializers.groups import GroupSerializer

class AdminView(ModelViewSet):

    serializer_class = AdminSerializer
    queryset = User.objects.all()
    pagination_class = PaginationNum
    permission_classes = [IsAdminUser]
    #获取用户组信息
    def simple(self,request):
        data = Group.objects.all()
        ser = GroupSerializer(data,many=True)
        return Response(ser.data)

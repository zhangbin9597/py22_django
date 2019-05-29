from meiduo_admin.serializers.users import UserShowList
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from users.models import User
from meiduo_admin.utils import PaginationNum
from django.db.models import Q
from rest_framework.permissions import IsAdminUser

class UservisitView(ListCreateAPIView):
    serializer_class = UserShowList
    queryset = User.objects.all()
    pagination_class = PaginationNum

    permission_classes = [IsAdminUser]
    #重写get_queryset
    def get_queryset(self):
        # 获取前端传来的数据
        user = self.request.query_params.get('keyword')
        if user is '' or user is None:
            return User.objects.all()
        else:
            return User.objects.filter(username=user)



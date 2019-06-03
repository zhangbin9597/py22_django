from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PaginationNum
from meiduo_admin.serializers.options import OptionSerializer,SPUSpecificationSerializer
from goods.models import SpecificationOption,SPUSpecification


class OptionView(ModelViewSet):
    serializer_class = OptionSerializer
    queryset = SpecificationOption.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PaginationNum

    def simple(self,request):
        data = SPUSpecification.objects.all()
        ser = SPUSpecificationSerializer(data,many=True)
        return Response(ser.data)

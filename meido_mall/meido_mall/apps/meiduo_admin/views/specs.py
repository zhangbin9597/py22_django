from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification,SPU
from meiduo_admin.serializers.specs import SPUSpecsSerializer,SPUSerializer
from meiduo_admin.utils import PaginationNum
from rest_framework.permissions import IsAdminUser



class SPUSpecView(ModelViewSet):
    serializer_class = SPUSpecsSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PaginationNum
    permission_classes = [IsAdminUser]

    def simple(self,request):
        spus = SPU.objects.all()
        ser = SPUSerializer(spus,many=True)
        return Response(ser.data)
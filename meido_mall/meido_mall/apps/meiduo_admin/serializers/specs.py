from rest_framework import serializers

from goods.models import SPUSpecification,SPU
from rest_framework.serializers import ModelSerializer

class SPUSpecsSerializer(ModelSerializer):
    # 规格序列化器

    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    class Meta:
        model = SPUSpecification
        fields = '__all__'

class SPUSerializer(ModelSerializer):

    class Meta:
        model = SPU
        fields = ('id','name')
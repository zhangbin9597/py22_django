from rest_framework import serializers

from goods.models import SPUSpecification,SPU
from rest_framework.serializers import ModelSerializer

class SPUSpecsSerializer(ModelSerializer):
    # 规格序列化器
    # create_time = serializers.DateTimeField()
    # update_time = serializers.DateTimeField()
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    class Meta:
        model = SPUSpecification
        fields = '__all__'

    # def create(self, validated_data):
    #     spec = SPUSpecification.objects.create(**validated_data)
    #     return spec
class SPUSerializer(ModelSerializer):
    # create_time = serializers.DateTimeField()
    # update_time = serializers.DateTimeField()
    class Meta:
        model = SPU
        fields = ('id','name')
from rest_framework import serializers
from goods.models import GoodsChannel,GoodsChannelGroup,GoodsCategory


class GoodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=GoodsChannelGroup
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    category_id=serializers.IntegerField()
    group_id=serializers.IntegerField()
    class Meta:
        model=GoodsChannel
        fields = '__all__'


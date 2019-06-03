from rest_framework import serializers
from orders.models import OrderInfo,OrderGoods
from goods.models import SKU

class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ('name','default_image')

class OrderGoodSerializer(serializers.ModelSerializer):
    sku = SKUSerializer(read_only=True)
    class Meta:
        model = OrderGoods
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    skus = OrderGoodSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'

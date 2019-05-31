from django.db import transaction
from rest_framework import serializers
from goods.models import SKU,GoodsCategory,SPUSpecification,SpecificationOption,SKUSpecification


class SKUSpecificationSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField(write_only=True)
    option_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')

class SKUSerializer(serializers.ModelSerializer):

    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    specs = SKUSpecificationSerializer(read_only=True)
    class Meta:
        model = SKU
        fields = '__all__'
        read_only_fields = ('spu','category')

    def create(self, validated_data):

        specs = self.context['request'].data.get('specs')
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                # 保存sku表
                sku = SKU.objects.create(**validated_data)
                #保存sku具体规格
                for spec in specs:
                    SKUSpecification.objects.create(spec_id=spec['spec_id'],option_id=spec['option_id'],sku=sku)
            except:
                #事务回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:
                transaction.savepoint_commit(save_point)
                return sku

    def update(self, instance, validated_data):

        # 或取前端传的数据 specs
        specs = self.context['request'].data.get('specs')

        with transaction.atomic():
            # 开启事务
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 修改sku表
                SKU.objects.filter(id=instance.id).update(**validated_data)
                # 修改sku具体规格
                for spec in specs:
                    SKUSpecification.objects.filter(sku=instance).update(**spec)
            except:
                # 事务回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')
            else:

                # 静态化生成详情页页面
                # get_detail_html.delay(instance.id)
                transaction.savepoint_commit(save_point)

                return instance
class GoodcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = '__all__'

class SpecificationOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificationOption
        fields = '__all__'

class SPUSpecificationSerializer(serializers.ModelSerializer):

    #嵌套返回 主表返回副表的数据
    options = SpecificationOptionSerializer(many=True)
    class Meta:
        model = SPUSpecification
        fields = '__all__'



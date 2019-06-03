from goods.models import SpecificationOption,SPUSpecification
from rest_framework import serializers


class SPUSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    spec = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SpecificationOption
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.models import Group


# class ContentTypeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ContentType
#         fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



from rest_framework import serializers
from users.models import User


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs={
            'password':{
                'write_only':True
            }

        }

    # 父类create方法保存时没有密码加密，重写父类方法增加密码加密
    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_staff = True
        user.set_password(validated_data['password'])
        user.save()
        return user
    # 父类update方法保存时没有密码加密，重写父类方法增加密码加密
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
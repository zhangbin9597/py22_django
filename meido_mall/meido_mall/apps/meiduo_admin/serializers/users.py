from users.models import User
from rest_framework.serializers import ModelSerializer

class UserShowList(ModelSerializer):
    '''用户序列化器'''
    class Meta:
        model = User
        fields = ('id','username','mobile','email','password')
        extra_kwarge={
            'username':{
                'max_length':15,
                'min_length':6
            },
            'password':{
                'max_lenght':15,
                'min_length':6,
                'write_only': True
            },
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

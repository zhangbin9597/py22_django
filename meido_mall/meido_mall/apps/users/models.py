from django.db import models
from django.contrib.auth.models import AbstractUser
from meido_mall.utils.models import BaseModel
from areas.models import Area
# Create your models here.


class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    #邮箱是否激活
    email_active = models.BooleanField(default=False)
    default_address = models.ForeignKey('Address',related_name='users',null=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# class Address(BaseModel):
#     user = models.ForeignKey(User,related_name='addresses')
#     title = models.CharField(max_length=20)
#     receiver = models.CharField(max_length=20)
#     province = models.ForeignKey(Area,related_name='provinces')
#     city = models.ForeignKey(Area,related_name='cities')
#     district = models.ForeignKey(Area,related_name='districts')
#     place = models.CharField(max_length=50)
#     mobile = models.CharField(max_length=11)
#     phone = models.CharField(max_length=20,null=True)
#     email = models.CharField(max_length=30,null=True)
#     is_delete = models.BooleanField(default=False)



class Address(BaseModel):
    # 用户
    user = models.ForeignKey(User, related_name='addresses')
    # 标题
    title = models.CharField(max_length=10)
    # 收件人
    receiver = models.CharField(max_length=10)
    # 省
    province = models.ForeignKey(Area, related_name='provinces')
    # 市
    city = models.ForeignKey(Area, related_name='cities')
    # 区县
    district = models.ForeignKey(Area, related_name='districts')
    # 详细地址
    detail = models.CharField(max_length=50)
    # 收件人手机号
    mobile = models.CharField(max_length=11)
    # 电话
    phone = models.CharField(max_length=20)
    # 邮箱
    email = models.CharField(max_length=50)
    # 逻辑删除
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_address'
        ordering = ['-update_time']

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'receiver': self.receiver,
            'province_id': self.province_id,
            'province': self.province.name,
            'city_id': self.city_id,
            'city': self.city.name,
            'district_id': self.district_id,
            'district': self.district.name,
            'place': self.detail,
            'mobile': self.mobile,
            'tel': self.phone,
            'email': self.email
        }




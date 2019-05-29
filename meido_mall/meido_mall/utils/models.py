import datetime
from django.db import models

class BaseModel(models.Model):
    """
    封装模型类中的公有属性:创建时间,修改时间
    注意:这个模型类不需要创建表
    """
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 当前模型类为抽象类,用于继承,不需要创建表
        abstract = True
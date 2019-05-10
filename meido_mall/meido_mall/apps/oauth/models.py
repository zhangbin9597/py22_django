from django.db import models
from users.models import User
from meido_mall.utils.models import BaseModel
# Create your models here.

class OAUthQQUser(BaseModel):
    user = models.ForeignKey(User)
    openid = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_oauth_qq'




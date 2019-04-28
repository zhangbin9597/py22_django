from django.db import models

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self',null=True,related_name='sbus')

    class Meta:
        db_table = 'tb_areas'



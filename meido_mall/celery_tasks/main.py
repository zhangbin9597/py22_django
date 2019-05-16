import os

os.environ["DJANGO_SETTINGS_MODULE"] = "meido_mall.settings.dev"

# celery启动文件
from celery import Celery

# 创建celery实例
app = Celery('meido')

# 加载celery配置
app.config_from_object("celery_tasks.config")

# 自动注册celery的任务
app.autodiscover_tasks([
    "celery_tasks.sms",
    "celery_tasks.mail",
    "celery_tasks.detail",
])
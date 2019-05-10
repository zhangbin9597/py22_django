# bind:保证task对象会作为第一个参数自动传入
# name:异步任务别名
# retry_backoff:异常自动重试的时间间隔 第n此(retry_backoff*2^(n-1))s
# max_retries:异常自动重试次数的上限
from celery_tasks.main import app
from meido_mall.libs.yuntongxun.sms import CCP



@app.task(bind=True,name='send_sms', retry_backoff = 3)
def send_sms(self, to, datas, tempid):
    """
    发送短信异步任务
    :param self:
    :param mobile:手机号
    :param sms_code: 短信验证码
    :return: 成功0 或者 失败-1
    """
    try:
        ccp = CCP()
        ret = ccp.send_template_sms(to,datas,tempid)
        print(datas[0])
    except Exception as e:
        self.retry(exc=e, max_retries= 3 )
    return ret

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

def dumps(json,expires):
    """
    加密
    :param json:字典
    :param expires:加密数据的过期时间
    :return: 字符串
    """
    # 1 创建工具对象
    serializer = Serializer(settings.SECRET_KEY,expires)
    # 2加密
    s1 = serializer.dumps(json)
    # 3 转字符串,返回
    return s1.decode()

def loads(s1,expires):
    """
    解密
    :param s1:字符串
    :param expires:加密数据过期时间
    :return: 字典
    """
    #1 创建工具对象
    serializer = Serializer(settings.SECRET_KEY,expires)
    #2 解密
    try:
        json = serializer.loads(s1)
    except:
        return None
    #3 返回字典
    return json


import pickle
import base64


def dumps(dict1):
    # 将字典转换成字符串
    # 1.转字节
    dict_bytes = pickle.dumps(dict1)
    # 2.加密
    str_bytes = base64.b64encode(dict_bytes)
    # 3.转字符串
    return str_bytes.decode()


def loads(str1):
    # 将字符串转换成字典
    # 1.转字节
    str_bytes = str1.encode()
    # 2.解密
    dict_bytes = base64.b64decode(str_bytes)
    # 3.转字典
    return pickle.loads(dict_bytes)

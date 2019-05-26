from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from datetime import date, timedelta

from meiduo_admin.serializers.statistical import GoodsSerializer
from users.models import User
from goods.models import GoodsVisitCount

class UserTotalCount(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]
    def get(self,request):

        #1.查询所有用户总量
        count = User.objects.all().count()
        #2.获取当前时间
        now_date = date.today()
        #3.返回
        return Response({
            'count':count,
            'date':now_date
        })

class DayCreateCount(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日注册用户数量 date_joined 记录创建账户时间
        count = User.objects.filter(date_joined__gte=now_date).count()
        return Response({
            "count": count,
            "date": now_date
        })


class UserActiveCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日登录用户数量  last_login记录最后登录时间
        count = User.objects.filter(last_login__gte=now_date).count()
        return Response({
            "count": count,
            "date": now_date
        })


class UserOrderCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日下单用户数量  orders__create_time 订单创建时间
        count = User.objects.filter(orders__create_time__gte=now_date).count()
        return Response({
            "count": count,
            "date": now_date
        })

class UserMonthCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取一个月前日期
        start_date = now_date - timedelta(29)
        # 创建空列表保存每天的用户量
        date_list = []

        for i in range(30):
            # 循环遍历获取当天日期
            index_date = start_date + timedelta(days=i)
            # 指定下一天日期
            cur_date = start_date + timedelta(days=i + 1)
            # 查询条件是大于当前日期index_date，小于明天日期的用户cur_date，得到当天用户量
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()

            date_list.append({
                'count': count,
                'date': index_date
            })

            return Response(date_list)

class GoodsDayView(APIView):

    def get(self,request):
        # 获取当天日期
        now_date=date.today()
        # 获取当天访问的商品分类数量信息
        data=GoodsVisitCount.objects.filter(date=now_date)
        # 序列化返回分类数量
        ser=GoodsSerializer(data,many=True)

        return Response(ser.data)
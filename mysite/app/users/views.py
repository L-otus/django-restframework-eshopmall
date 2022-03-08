from django.shortcuts import render
from .models import User, coupon,coupon_use,Adress,Token
from .serializer import coupon_serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from utils import wx_auth
import uuid,rest_framework,requests,json

appid = ''
AppSecret = ''

#微信用户登录视图
class loginview(APIView):
    def post(self, request):
        #wx.login()的code
        request_data=request.data
        code=request_data.get('code', '')
        if not code:
            return Response({'error': '没有收到code'},status=400)
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=&secret=&js_code='+code+'&grant_type=authorization_code'
        try:
            res=requests.get(url)
        except Exception as e:
            return Response({'error':'向微信request失败'},status=500)
        try:
            res.encoding = 'utf-8'
        except Exception as e:
            return Response({'error':'编码失败'},status=500)
        try:
            r_list = res.text
        except Exception as e:
            return Response({'error':'text方法失败'},status=500)
        try:
            j_list = json.loads(r_list)
        except Exception as e:
            return Response({'error':'json.loads出错'},status=500)
        try:
            openid = j_list.get('openid', '')
        except Exception as e:
            return Response({'error':'get openid出错'},status=500)
        # 判断是否是正确的openid
        if not openid:
            erc=j_list.get('erc')
            msg=j_list.get('msg')
            return Response({'error': 'openid为空','erc':erc,'msg':msg},status=500)
        # 验证数据库是否存在该用户,判断其状态是否激活
        user_obj_false = User.objects.filter(wxopenid=openid, activation=False).first()
        if user_obj_false:
            return Response({'error': '该用户已存在但未激活'},status=500)
        # 验证数据库是否存在该用户,不存在则创建
        try:
            user_obj = User.objects.filter(wxopenid=openid, activation=True).first()
        except Exception as e:
            return Response({'error':'查询用户出错'},status=500)
        token = uuid.uuid4()
        if not user_obj:
            # 创建用户，返回token
            try:
                user_obj_code = User.objects.create(user_json=code, wxopenid=openid)
            except Exception as e:
                return Response({'error':'创建用户出错'},status=500)
            try:
                Token.objects.create(token=token, user=user_obj_code)
            except Exception as e:
                return Response({'error':'创建token出错'},status=500)
            return Response({'userID': user_obj_code.id,'userOPENID':user_obj_code.wxopenid,'token': token})
        # 如果存在该用户，则更新token后返回
        else:
            try:
                Token.objects.filter(user=user_obj).update(token=token)
            except Exception as e:
                return Response({'error': '登录失败'},status=500)
            return Response({
                    'userID':user_obj.id,
                    'userOPENID': user_obj.wxopenid,
                    'token': token})
#优惠券查询
class coupounviews(APIView):
    def get(self, request):
        user_id=request.query_params.get('userID')
        #传递用户id
        status=request.query_params.get('status')
        #传递需要查询的优惠券的状态
        try:
            status=int(status)
        except Exception as e:
            print(e)
            print(status)
            return Response({'error':'无法转换为int类型'},status=500)

        if (status>3 or status<1):
            return Response({'error': '优惠券状态参数错误'},status=400)

        if not user_id:
            return Response({'error': '传递userID为空'},status=400)
        if isinstance(user_id,int):
            return Response({'error':'传递的userid应当为数字'},status=400)
        else:
            try:
                coupon_get = coupon_use.objects.filter(user_id=user_id)
                if user_id and status:
                    coupon_get = coupon_use.objects.filter(user_id=user_id,status=status)
                if not coupon_get:
                    return Response([])
                serial = coupon_serializer(coupon_get, many=True)
                return Response(serial.data)
            except Exception as e:
                print(e)
                return Response({'error': '服务器查找优惠券错误'},status=500)

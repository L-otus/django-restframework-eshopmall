from django.shortcuts import render
from .models import good,good_attribute,machine_address,order,order_good
from .serializer import goodserializer,orderserializer,distributeserializer,orderstatusserializer,\
    recommendserializer,recommendgoodserializer,machineserializer,orderbyuserserializer,imageserializer
from app.users.models import coupon_use,coupon
from app.goods import itemcf
from mysite import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.utils.timezone import now
import uuid,datetime,qrcode,random
# Create your views here.

totaldishes=35#菜品总数

class orderingview(APIView):
    def post(self, request):


        try:
            time_now_str=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S%f')
            time_str=datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S%f')
            time=datetime.datetime.now()
            orderuuid=str(uuid.uuid1())
            orderIDwithtime='{0}{1}{2}'.format('chuiyan',orderuuid,time_now_str)
        except Exception as e:
            print(e)
            return Response({'error':'创建时间失败'},status=500)

        try:
            req_data=request.data
            userID=req_data.get('userID','')

            #菜品组
            goodsGroup=req_data.get('goods','')
            items=len(goodsGroup)

            #优惠券
            couponID=req_data.get('couponID','')

            #售货机id
            machineID=req_data.get('machineID','')

            #订单金额
            totalprice=req_data.get('totalprice','')
            totalprice=float(totalprice)

            #订单备注
            note=req_data.get('note','')
            #
            phone=req_data.get('phone')

        except Exception as e:
            print(e)
            return Response({'error': '传递参数出错'}, status=500)

        address_obj=machine_address.objects.filter(machine_id=machineID).first()
        pickup_address_poly=address_obj.title

        if not (isinstance(couponID,int)):
            return Response({'error':'传递的优惠券id不是int类型'},status=400)
        try:
            if (couponID):
                coupon_obj=coupon_use.objects.filter(id=couponID).first()
                if(coupon_obj.status!=1):
                    return Response({'error':'该订单使用的优惠券不可用'},status=400)
                coupon_obj=coupon_use.objects.filter(id=couponID).update(status=2)
        except Exception as e:
            print(e)
            return Response({'error':'更新优惠券状态失败'},status=500)



        try:
            # 二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=15,
                border=4,
            )
            qr.add_data(orderIDwithtime)
            qr.make()
            # 二维码保存
            qr_img = qr.make_image()
            file_dir = '{0}{1}{2}'.format(settings.MEDIA_ROOT, time_str, '.jpg')
            file_url='{0}{1}{2}'.format(settings.MEDIA_URL, time_str, '.jpg')
            qr_img.save(file_dir)
        except Exception as e:
            print(e)
            return Response({'error':'二维码生成出错'},status=500)

        try:
            # 订单数据
            order_data={
                'user_id':userID,
                'order_uid':orderIDwithtime,
                'order_price':totalprice,
                'order_status':2,
                'order_pickup_machine_id':machineID,
                'order_pickup_machine_address':pickup_address_poly,
                'qr_path':file_url,
                'order_note':note,
                'phone_num':phone
            }
            # 保存订单
            order_obj = order.objects.create(**order_data)
            orderID=order_obj.id
        except Exception as e:
            print(e)
            coupon_obj = coupon_use.objects.filter(id=couponID).update(status=1)
            return Response({'error':'订单保存出错'},status=500)

        try:
            rest_amount=[]
            update_set=[]

            for i in range(items):
                goodID = goodsGroup[i].get('goodID', '')
                goodAmount = goodsGroup[i].get('goodAmount', '')
                # 选择咸度、辣度
                salty = goodsGroup[i].get('salty')
                spicy = goodsGroup[i].get('spicy')
                if(salty<0)or(salty>4):
                    return Response({'error':'传递咸度的数字必须在0-4之间'},status=400)
                if(spicy<0)or(spicy>4):
                    return Response({'error': '传递辣度的数字必须在0-4之间'}, status=400)
                #逐个查找订单中对应ID的菜品
                try:
                    good_obj = good_attribute.objects.filter(good_id=goodID).first()
                    if not good_obj:
                        return Response({'error': '查找不到对应ID的菜品1'}, status=500)
                except Exception as e:
                    print(e)
                    return Response({'error': '外键反向引用出错'}, status=500)
                #查找成功后查找该菜品对应的调料表
                try:
                    ing_id=good_obj.ingredient_id
                except Exception as e:
                    print(e)
                    return Response({'error':'查找对应调料包出错'},status=500)

                try:
                    if (goodAmount > good_obj.amount):
                        mistake_order=order.objects.filter(id=orderID).update(order_status=6)
                        coupon_obj = coupon_use.objects.filter(id=couponID).update(status=1)
                        return Response({'error': '下单数量大于库存'}, status=400)
                        # 菜品库存不够
                    else:
                        order_good_data = {
                            'order_id': orderID,
                            'good_id': goodID,
                            'good_orderAmount': goodAmount,
                            'alt_salty':salty,
                            'alt_spicy':spicy,
                            'ingredient_id':ing_id
                        }
                        order_good_object = order_good.objects.create(**order_good_data)
                        rest=good_obj.amount-goodAmount
                        good_obj = good_attribute.objects.filter(good_id=goodID)
                        rest_amount.append(rest)
                        update_set.append(good_obj)

                except Exception as e:
                    print(e)
                    return Response({'error': '录入订单的菜品失败'}, status=500)
            length1=len(update_set)
            length2=len(rest_amount)
            if(length1!=length2):
                return Response({'error':'更新数据组与更新集长度不一致'},status=500)
            try:
                for i in range(length1):
                    update_set[i].update(amount=rest_amount[i])
            except Exception as e:
                print(e)
                return Response({'error':'更新出错'})
            return Response({'success': '保存订单成功', 'order_uid': orderIDwithtime})
        except Exception as e:
            print(e)
            return Response({'error':'订单菜品录入出错'},status=500)
#返回固定订单号
class orderfindview(APIView):
    def get(self,request):
        orderfind_id=request.query_params.get('order_uid')
        orderfind_obj=order.objects.filter(order_uid=orderfind_id).first()
        find_ser=orderserializer(orderfind_obj)
        if(find_ser):
            return Response(find_ser.data)
        else:
            return Response({'error':'查询数据库中的订单出错'},status=500)

class orderfindbyuserView(APIView):
    def get(self,request):
        userID=request.query_params.get('userID')
        status=request.query_params.get('status')
        queryset=order.objects.filter(user_id=userID,order_status=status).all()
        try:
            ser=orderbyuserserializer(instance=queryset,many=True)
        except Exception as e:
            print(e)
            return Response({'error':'序列化错误'},status=500)
        return Response(ser.data)

class goodfindbycategory1View(APIView):
    def get(self,request):
        category=request.query_params.get('category')
        print(category)
        try:
            category=int(category)
        except Exception as e:
            print(e)
            return Response({'error':'category参数必须为数字'},status=400)
        if(category<1)or(category>4):
            return Response({'error':'类型数必须在1-4之间'},status=400)
        queryset=good_attribute.objects.filter(goods_type1=category).all()
        if(queryset):
            try:
                ser=goodserializer(instance=queryset,many=True)
            except Exception as e:
                print(e)
                return Response({'error':'序列化错误'},status=500)
            return Response(ser.data)
        else:
            return Response({'error':'按菜系查找出错'},status=400)

class goodfindbycategory2View(APIView):
    def get(self,request):
        category=request.query_params.get('category')
        try:
            category=int(category)
        except Exception as e:
            print(e)
            return Response({'error':'category参数必须为数字'},status=400)
        if(category<1)or(category>4):
            return Response({'error':'类型数必须在1-4之间'},status=400)
        queryset=good_attribute.objects.filter(goods_type2=category).all()
        if(queryset):
            try:
                ser=goodserializer(instance=queryset,many=True)
            except Exception as e:
                print(e)
                return Response({'error':'序列化错误'},status=500)
            return Response(ser.data)
        else:
            return Response({'error':'按锅具查找出错'},status=400)



#返回所有菜品
class goodfindview(APIView):
    def get(self, request):
        queryset=good_attribute.objects.all()
        findserial=goodserializer(instance=queryset,many=True)
        if(findserial):
            return Response(findserial.data)
        else:
            return Response({'error':'查询数据库中的菜品出错'},status=500)

#stm-32扫码返回订单号查询检验
class machinequeryview(APIView):
    def get(self,request):
        try:
            ordercheck_id=request.query_params.get('order_uid')
        except Exception as e:
            print(e)
            return Response({'error':'无法从get请求中获得order_uid参数'},status=400)
        try:
            ordercheck=order.objects.filter(order_uid=ordercheck_id).first()
        except Exception as e:
            print(e)
            return Response({'error':'没有该id对应的订单'},status=400)
        status=ordercheck.order_status
        if (status!=2):
            statusser=orderstatusserializer(ordercheck)
            return Response({'error':statusser.data},status=400)

        dsser=distributeserializer(ordercheck)
        if(dsser):
            return Response(dsser.data)
        else:
            return Response({'error':'序列化出错'},status=500)
#stm-32出货成功
class deliversuccessview(APIView):
    def post(self,request):
        try:
            ordercheck_id=request.data.get('order_uid')
            orderchange_status=request.data.get('status')
        except Exception as e:
            print(e)
            return Response({'error':'无法获取传递的参数'},status=400)
        if not (isinstance(orderchange_status,int)):
            return Response({'error':'传递状态参数不是数字'},status=400)
        try:
            ordercheck=order.objects.filter(order_uid=ordercheck_id).first()
        except Exception as e:
            print(e)
            return Response({'error':'没有该id对应的订单'},status=400)
        orderstatus=ordercheck.order_status
        if (orderstatus!=2):
            statusser=orderstatusserializer(ordercheck)
            return Response({'error':statusser.data},status=400)
        try:
            if(orderchange_status):
                ordercheck=order.objects.filter(order_uid=ordercheck_id).update(order_status=3)
                return Response(status=200)
        except Exception as e:
            print(e)
            return Response({'error':'更新订单状态出错'})

class recommendView(APIView):
    def get(self,request):
        try:
            user_id=request.query_params.get('userID')
            print(user_id)
            user_id=int(user_id)
            if(user_id==0):
                datas=itemcf.rec(29)
                print(datas)
            else:
                orderfind=order.objects.filter(user_id=user_id,order_status=2).order_by('-create_time').first()
                print(orderfind)
                if not(orderfind):
                    datas=itemcf.rec(28)
                else:
                    ser=recommendserializer(orderfind)
                    datas=ser.data.get('goodID')
                    print(datas)
        except Exception as e:
            print(e)
            return Response({'error':'无法获得推荐'},status=500)
        rec=[]
        for i in range(4):
            goodfind=good.objects.filter(good_id=datas[i]).first()
            ser1=recommendgoodserializer(goodfind)
            rec.append(ser1.data)
        return Response({'recoomendation':rec})
#返回机器地址
class machineaddressView(APIView):
    def get(self,request):
        queryset=machine_address.objects.all()
        try:
            ser=machineserializer(instance=queryset,many=True)
        except Exception as e:
            print(e)
            return Response({'error':'序列化出错'})
        return Response(ser.data)

class imgView(APIView):
    def get(self,request):
        n=[random.randint(0,totaldishes) for _ in range(4)]
        url=[]
        for item in n:
            image_good=good.objects.filter(id=item).first()
            ser=imageserializer(image_good)
            url.append(ser.data)
        return Response({'urls':url})
from rest_framework import serializers
from .models import good,good_attribute,ingredients,order,order_good,machine_address
import datetime
from app.goods import itemcf

class goodserializer(serializers.ModelSerializer):
    goodser=serializers.SerializerMethodField()
    type1=serializers.SerializerMethodField()
    type2=serializers.SerializerMethodField()
    class Meta:
        model=good_attribute
        fields=['goodser','rec_salt','rec_amount','price','type1','type2']
        depth=1
    def get_goodser(self,obj):
        good_obj=obj.good
        return {
            'goodsID':good_obj.good_id,
            'goodAmount':good_obj.good_name,
            'goodDescription':good_obj.good_description,
            'goodImgURL':good_obj.good_img,
            'goodStatus':good_obj.good_sale_status,
        }
    def get_type1(self,obj):
        return obj.get_goods_type1_display()
    def get_type2(self,obj):
        return obj.get_goods_type2_display()

class goodcategoryserializer(serializers.ModelSerializer):
    goodser=serializers.SerializerMethodField()
    class Meta:
        model=good_attribute
        fields=['goodser','rec_salt','rec_amount','price']
        depth=1
    def get_goodser(self,obj):
        good_obj=obj.good
        return {
            'goodsID':good_obj.good_id,
            'goodAmount':good_obj.good_name,
            'goodDescription':good_obj.good_description,
            'goodImgURL':good_obj.good_img,
            'goodStatus':good_obj.good_sale_status
        }


class orderserializer(serializers.ModelSerializer):
    ordergood_ser=serializers.SerializerMethodField()
    class Meta:
        model=order
        fields=['order_pickup_machine_address','create_time','qr_path','order_note','order_price','phone_num','ordergood_ser']
        depth=1
    def get_ordergood_ser(self,obj):
        ordergood_list=obj.ordered_good.all()
        res=[]
        for item in ordergood_list:
            item_name=item.good.good_name+'炒料'
            item_url=item.good.ingredient_img_url
            id=item.good_id
            goodobj=good_attribute.objects.filter(good_id=id).first()
            price=goodobj.price
            res.append({
                'ingredientsURL':item_url,
                'ingredientsNAME':item_name,
                'unit_price':price,
                'Amount':item.good_orderAmount
            })
        return res

class orderbyuserserializer(serializers.ModelSerializer):
    ing=serializers.SerializerMethodField()
    orderstatus=serializers.SerializerMethodField()
    class Meta:
        model=order
        fields=['order_uid','order_pickup_machine_address','orderstatus','create_time','order_price','ing']
        depth=1
    def get_ing(self,obj):
        ordergood = obj.ordered_good.first()
        item_name=ordergood.good.good_name+'炒料'
        item_url = ordergood.good.ingredient_img_url
        return {
                'ingredientsURL': item_url,
                'ingredientsNAME': item_name,
                'salt&spicy':[ordergood.alt_salty,ordergood.alt_spicy]
        }
    def get_orderstatus(self,obj):
        return obj.get_order_status_display()


class distributeserializer(serializers.ModelSerializer):
    ingredient_ser=serializers.SerializerMethodField()
    class Meta:
        model=order
        fields=['ingredient_ser']
    def get_ingredient_ser(self,obj):
        res=[]
        ordergood_list=obj.ordered_good.all()
        for item in ordergood_list:
            sal=item.ingredient.salt
            alc=item.ingredient.alc
            thinsoy=item.ingredient.thinsoy
            vinegar=item.ingredient.vinegar
            thicksoy=item.ingredient.thicksoy
            sugar=item.ingredient.sugar
            pepper= item.ingredient.pepper
            aginomoto=item.ingredient.aginomoto
            res.append({
                "pack1":[sal,0,0,0,0,sugar,pepper,aginomoto],
                "pack2":[0,alc,thinsoy,vinegar,thicksoy,0,0,0],
                "pack3":[0,0,0,0,0,0,0,0],
                "pack4": [0, 0, 0, 0, 0, 0, 0, 0],
                "num":item.good_orderAmount
            })
        return res

class orderstatusserializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    class Meta:
        model=order
        fields=['status']
    def get_status(self,obj):
        return {'订单状态':obj.get_order_status_display()}

class recommendserializer(serializers.ModelSerializer):
    goodID=serializers.SerializerMethodField()
    class Meta:
        model=order
        fields=['goodID']
    def get_goodID(self,obj):
        ordergood=obj.ordered_good.first()
        goodid=ordergood.good_id
        recid=itemcf.rec(goodid)
        return recid

class recommendgoodserializer(serializers.ModelSerializer):
    class Meta:
        model=good
        fields=['good_name','good_img']


class machineserializer(serializers.ModelSerializer):
    machine=serializers.SerializerMethodField()
    class Meta:
        model=machine_address
        fields=['machine']
    def get_machine(self,obj):
        pickup_address_poly = '{0}{1}{2}{3}'.format(obj.province, obj.city, obj.district,
                                                    obj.detailed_address)
        location=[float(obj.longitude),float(obj.latitude)]
        return {
            'machine_id':obj.id,
            'center':location,
            'name':obj.title,
            'detailAddress':pickup_address_poly,
            'phone':obj.phone_number,
            'workTime':obj.available_time
        }

class imageserializer(serializers.ModelSerializer):
    class Meta:
        model=good
        fields=['good_img']
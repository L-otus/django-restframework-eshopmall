from django.db import models

#调料类
class ingredients(models.Model):
    salt=models.FloatField(verbose_name='盐量')
    alc=models.FloatField(verbose_name='料酒量')
    thinsoy=models.FloatField(verbose_name='生抽量')
    vinegar=models.FloatField(verbose_name='醋量')
    thicksoy=models.FloatField(verbose_name='老抽量')
    sugar=models.FloatField(verbose_name='糖量')
    pepper=models.FloatField(verbose_name='花椒量')
    aginomoto=models.FloatField(verbose_name='味精量')

    class Meta:
        verbose_name='21-调料表'
        verbose_name_plural=verbose_name

#商品类
class good(models.Model):
    good_id=models.CharField(max_length=64,unique=True,verbose_name='商品id')
    good_name=models.CharField(max_length=64,verbose_name='商品名')
    good_description=models.CharField(max_length=64,verbose_name='商品描述')
    good_img=models.TextField(verbose_name='商品图片')
    ingredient_img_url = models.TextField(verbose_name='调料包图片url')
    good_sale_status=models.BooleanField(default=True,verbose_name='是否上架')

    class Meta:
        verbose_name='11-商品表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.good_name
'''
class good_detail(models.Model):
    detail_description=models.CharField(null=True,verbose_name='商品详情描述')
    swing_img = models.CharField(verbose_name='轮播图')
    goods=models.OneToOneField(to=good,on_delete=False,verbose_name='关联商品')
    goods_title=models.CharField(max_length=64,verbose_name='商品标题')

    class Meta:
        verbose_name='12-商品详情表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.goods_title
'''
class good_attribute(models.Model):
    attribute_id=models.IntegerField(verbose_name='属性id',null=True)
    good = models.ForeignKey(to=good, related_name='goodattr', on_delete=models.CASCADE, verbose_name='对应商品')
    rec_salt=models.IntegerField(verbose_name='推荐商品咸度')
    rec_amount=models.IntegerField(verbose_name='推荐商品分量')
    goods_category1=((1,'川'),(2,'鲁'),(3,'粤'),(4,'其他'))
    goods_category2=((1,'平底锅'),(2,'汤锅'),(3,'微波炉'),(4,'电饭煲'))
    goods_type1=models.IntegerField(choices=goods_category1,verbose_name='菜系')
    goods_type2 = models.IntegerField(choices=goods_category2, verbose_name='锅具')
    #salt=models.CharField(max_length=16,verbose_name='商品咸度')
    amount=models.IntegerField(verbose_name='商品库存')
    price=models.FloatField(max_length=64,verbose_name='价格')
    #detail=models.ForeignKey(to=good_detail,on_delete=models.CASCADE,verbose_name='关联详情')
    ingredient=models.ForeignKey(to=ingredients,on_delete=False,verbose_name='调料内容',unique=True)


    class Meta:
        verbose_name='13-商品属性表'
        verbose_name_plural=verbose_name


class machine_address(models.Model):
    title=models.CharField(max_length=16,verbose_name='售货机标题')
    province=models.CharField(max_length=16,verbose_name='售货机省份')
    city=models.CharField(max_length=16,verbose_name='售货机城市')
    district=models.CharField(max_length=16,verbose_name='售货机区')
    detailed_address=models.CharField(max_length=128,verbose_name='详细地址')
    machine_id=models.CharField(max_length=16,verbose_name='售货机号')
    available_time=models.CharField(max_length=16,verbose_name='营业时间')
    phone_number=models.CharField(max_length=32,verbose_name='联系电话')
    longitude=models.CharField(max_length=32,verbose_name='经度')
    latitude=models.CharField(max_length=32,verbose_name='纬度')

    class Meta:
        verbose_name='14-机器表'
        verbose_name_plural=verbose_name

class order(models.Model):
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,null=True,verbose_name='关联用户')
    order_uid=models.CharField(max_length=128,verbose_name='唯一订单号')
    order_price=models.FloatField(verbose_name='订单金额')
    order_status_choice=((1,'未支付'),(2,'已支付，待取货'),(3,'已出货'),(4,'已取消'),(5,'已退款'),(6,'异常订单'))
    order_status=models.IntegerField(choices=order_status_choice,verbose_name='订单状态')
    #order_address_user=models.ForeignKey('users.Address',on_delete=models.DO_NOTHING,verbose_name='关联地址')
    #order_address_machine=models.ForeignKey(to=machine_address,on_delete=models.DO_NOTHING,verbose_name='关联售货机地址')
    #order_discount=models.CharField(max_length=64,null=True,verbose_name='订单优惠金额')
    order_pickup_machine_id=models.CharField(max_length=32,verbose_name='取货机器号')
    order_pickup_machine_address=models.CharField(max_length=256,verbose_name='取货机详细地址')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='订单创建时间')
    completed_time=models.DateTimeField(null=True,verbose_name='订单完成时间')
    paid_time=models.DateTimeField(auto_now_add=True,verbose_name='支付完成时间')
    qr_path=models.TextField(verbose_name='二维码图片存储地址')
    order_note=models.CharField(max_length=32,null=True,verbose_name='订单备注')
    phone_num=models.CharField(max_length=16,verbose_name='手机号')

    class Meta:
        verbose_name='15-订单表'
        verbose_name_plural=verbose_name

class order_good(models.Model):
    order=models.ForeignKey(to=order,related_name='ordered_good',on_delete=models.CASCADE,verbose_name='对应订单')
    good=models.ForeignKey(to=good,on_delete=models.DO_NOTHING,verbose_name='下单菜品')
    good_orderAmount=models.IntegerField(verbose_name='下单数量')
    alt_salty=models.IntegerField(verbose_name='选择咸度')
    alt_spicy=models.IntegerField(verbose_name='选择辣度')
    ingredient=models.ForeignKey(to=ingredients,on_delete=models.DO_NOTHING,verbose_name='下单菜品的调料')

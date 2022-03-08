from django.db import models

# Create your models here.
"""
class tags(models.Model):
    flavour_choice=((1,'苦'),(2,'咸'),(3,'酸'),(4,'鲜'),(5,'甜'),(6,'辣'),(7,'麻'))
    taste_choice=((1,'硬'),(2,'脆'),(3,'软'),(4,'清淡'),(5,'重油盐'))
    pref_choice=((1,'中餐'),(2,'西餐'))
    pref2_choice=((1,'凉菜'),(2,'热菜'),(3,'早餐'),(4,'正餐'),(5,'饮品'),(6,'小吃'),(7,'粥点'),(8,'汤例'),(9,'点心'),(10,'素菜'),(11,'荤菜'))
    pref3_choice=((1,'海鲜'),(2,'飞禽'),(3,'家畜'))
    pref4_choice=((1,'煮'),(2,'焗'),(3,'蒸'),(4,'炒'),(5,'炸'),(6,'煎'),(7,'卤'),(8,'炖'),(9,'烤'),(10,'闷'),(11,'红烧'),(12,'拌'),(13,'烩'))
    flavour=models.IntegerField(choices=flavour_choice,verbose_name='口味')
    taste=models.IntegerField(choices=taste_choice,verbose_name='口感')
    pref1=models.IntegerField(choices=pref_choice,verbose_name='菜品')
    pref2=models.IntegerField(choices=pref2_choice,verbose_name='菜式')
    pref3=models.IntegerField(choices=pref3_choice,verbose_name='食材')
    pref4=models.IntegerField(choices=pref4_choice,verbose_name='烹饪方法')

    class Meta:
        verbose_name='06-用户标签'
        verbose_name_plural=verbose_name
"""
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名',null=True)
    wxopenid=models.CharField(max_length=32,verbose_name='微信openid',unique=True,default=None)
    user_json=models.CharField(max_length=32,verbose_name='用户json')
    login_time=models.DateTimeField(auto_now=True,verbose_name='登录时间')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(auto_now=True,verbose_name='最后一次更新时间')
    activation=models.BooleanField(default=True,verbose_name='激活状态')
    #user_tag=models.OneToOneField(to=tags,on_delete=True,verbose_name='用户偏好')
    class Meta:
        verbose_name='01-用户表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.wxopenid

class Adress(models.Model):
    city=models.CharField(max_length=32,verbose_name='市')
    province=models.CharField(max_length=32,verbose_name='省')
    district=models.CharField(max_length=32,verbose_name='区')
    user=models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='关联用户')

    def __str__(self):
        return'{}-{}-{}'.format(self.province,self.city,self.district)

    class Meta:
        verbose_name='02-地址表'
        verbose_name_plural=verbose_name

class coupon(models.Model):
    coupon_name=models.CharField(max_length=64,verbose_name='优惠券名')
    coupon_sub=models.CharField(max_length=64,verbose_name='优惠券描述')
    #coupon_valid_time=models.DateField(verbose_name='有效时间')
    coupon_invalid_time=models.DateField(verbose_name='失效时间')
    coupon_active_time=models.DateField(verbose_name='生效时间')
    coupon_create_time=models.DateField(auto_now_add=True,verbose_name='创建时间')
    coupon_price=models.FloatField(max_length=64,verbose_name='金额')

    class Meta:
        verbose_name='03-优惠券'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '{}-{}'.format(self.coupon_name,self.coupon_price)

class coupon_use(models.Model):
    coupon=models.ForeignKey(to=coupon,on_delete=models.CASCADE,verbose_name='优惠券')
    user=models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='绑定用户')
    status_choices=((1,'未使用'),(2,'已使用'),(3,'已过期'))
    status=models.IntegerField(choices=status_choices,verbose_name='优惠券状态')
    obtain_time=models.DateField(verbose_name='获得时间')
    used_time=models.DateField(verbose_name='使用时间',null=True,blank=True)

    class Meta:
        verbose_name='04-优惠券使用'
        verbose_name_plural=verbose_name
        unique_together=('user','coupon')

    def __str__(self):
        return '{}-{}'.format(self.coupon,self.status)

class Token(models.Model):
    token=models.UUIDField(verbose_name='token_uuid',default=None)
    create_time=models.DateField(auto_now=True,verbose_name='创建时间')
    user=models.OneToOneField(to=User,on_delete=False,verbose_name='关联用户')
    class Meta:
        verbose_name='05-用户token'
        verbose_name_plural=verbose_name
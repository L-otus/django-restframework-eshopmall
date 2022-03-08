from django.contrib import admin
from .models import User,Adress,coupon,coupon_use,Token
# Register your models here.

#admin.site.register(tags)
admin.site.register(User)
admin.site.register(coupon)
admin.site.register(coupon_use)
admin.site.register(Token)
admin.site.register(Adress)
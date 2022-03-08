from rest_framework import serializers
from .models import coupon_use

#优惠券
class coupon_serializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    detail=serializers.SerializerMethodField()

    class Meta:
        model=coupon_use
        fields=['status','detail']

    def get_status(self, obj):
        return obj.get_status_display()

    def get_detail(self,obj):
        couponobj=obj.coupon
        return {"coupon_name":couponobj.coupon_name,
                "coupon_price":couponobj.coupon_price,
                "coupon_invalid_time":couponobj.coupon_invalid_time,
                "coupon_sub":couponobj.coupon_sub}

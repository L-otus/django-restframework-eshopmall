from django.contrib import admin
from .models import ingredients,good,good_attribute,order,order_good,machine_address
# Register your models here.

admin.site.register(ingredients)
admin.site.register(good)
admin.site.register(good_attribute)
admin.site.register(order)
admin.site.register(order_good)
admin.site.register(machine_address)
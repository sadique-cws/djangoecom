from django.contrib import admin
from store.models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered_date','coupon','ordered','address']


class OrderItemAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    pass

class CouponAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item,ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)


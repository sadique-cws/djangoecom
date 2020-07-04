from django.contrib import admin
from store.models import *

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Coupon)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)


from django.contrib import admin
from .models.order import Order, OrderItem, OrderItemAttribute
# Register your models here.



admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemAttribute)
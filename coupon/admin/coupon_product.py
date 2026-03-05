from django.contrib import admin
from ..models import CouponProduct


@admin.register(CouponProduct)
class CouponProductAdmin(admin.ModelAdmin):
    list_display = ("coupon", "product")
    search_fields = ("coupon__code", "product__name")
    list_filter = ("coupon",)
    ordering = ("coupon__code", "product__name")

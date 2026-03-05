from django.contrib import admin
from ..models import CouponStore


@admin.register(CouponStore)
class CouponStoreAdmin(admin.ModelAdmin):
    list_display = ("coupon", "store")
    search_fields = ("coupon__code", "store__name")
    list_filter = ("coupon",)
    ordering = ("coupon__code", "store__name")

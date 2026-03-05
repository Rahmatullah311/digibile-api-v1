from django.contrib import admin
from ..models import CouponUsage


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ("coupon", "user", "order", "discount_amount", "used_at")
    search_fields = ("coupon__code", "user__username", "order__id")
    list_filter = ("coupon", "used_at")
    ordering = ("-used_at",)
    readonly_fields = ("coupon", "user", "order", "discount_amount", "used_at")

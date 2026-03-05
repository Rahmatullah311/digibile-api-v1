from django.contrib import admin
from ..models import CouponCategory


@admin.register(CouponCategory)
class CouponCategoryAdmin(admin.ModelAdmin):
    list_display = ("coupon", "category")
    search_fields = ("coupon__code", "category__name")
    list_filter = ("coupon",)
    ordering = ("coupon__code", "category__name")

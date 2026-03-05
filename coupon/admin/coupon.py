from django.contrib import admin
from ..models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "min_purchase",
        "valid_from",
        "valid_to",
        "active",
        "usage_limit",
        "used_count",
        "per_user_limit",
        "applicable_to_all",
    )
    list_filter = (
        "discount_type",
        "active",
        "valid_from",
        "valid_to",
    )
    search_fields = ("code", "description")
    readonly_fields = ("used_count", "created_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "description",
                    "discount_type",
                    "discount_value",
                    "min_purchase",
                )
            },
        ),
        (
            "Validity",
            {
                "fields": (
                    "valid_from",
                    "valid_to",
                    "active",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Usage Limits",
            {
                "fields": (
                    "usage_limit",
                    "used_count",
                    "per_user_limit",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Applicability",
            {
                "fields": (
                    "applicable_to_all",
                    # 'products',
                    # 'categories',
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

from rest_framework import serializers
from coupon.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "description",
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
            "created_at",
        ]
        read_only_fields = ["used_count", "created_at"]

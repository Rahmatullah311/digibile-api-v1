from rest_framework import serializers
from coupon.models import CouponUsage

class CouponUsageSerializer(serializers.ModelSerializer):
    # Optional: nested display of related fields
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = CouponUsage
        fields = [
            'id',
            'coupon',
            'coupon_code',
            'user',
            'user_email',
            'order',
            'order_id',
            'discount_amount',
            'used_at',
        ]
        read_only_fields = [
            'id',
            'coupon_code',
            'user_email',
            'order_id',
            'used_at',
        ]

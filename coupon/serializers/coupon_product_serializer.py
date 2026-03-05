from rest_framework import serializers
from coupon.models import CouponProduct
from product.serializers.product_serializer import ProductSerializer
from product.models.product import Product


class CouponProductCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CouponProduct
        fields = [
            "id",
            "coupon",
            "product",
            "product_id",
        ]
        read_only_fields = [
            "id",
            "product",
        ]


class CouponProductDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CouponProduct
        fields = [
            "id",
            "coupon",
            "product",
        ]
        read_only_fields = [
            "id",
            "coupon",
            "product",
        ]

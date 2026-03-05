from rest_framework import serializers
from coupon.models import CouponCategory
from product.serializers.category_serializer import CategorySerializer


class CouponCategoryCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=CategorySerializer.Meta.model.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = CouponCategory
        fields = [
            "id",
            "coupon",
            "category_id",
        ]


class CouponCategoryDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = CouponCategory
        fields = [
            "id",
            "coupon",
            "category",
        ]
        read_only_fields = ["id"]

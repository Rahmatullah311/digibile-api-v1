from rest_framework import serializers
from coupon.models import CouponStore
from store.serializers.store_serializer import StoreSerializer



class CouponStoreCreateSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=StoreSerializer.Meta.model.objects.all(),
        source="store",
        write_only=True,
    )

    class Meta:
        model = CouponStore
        fields = [
            "id",
            "coupon",
            "store_id",
        ]


class CouponStoreDetailsSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = CouponStore
        fields = [
            "id",
            "coupon",
            "store",
        ]
        read_only_fields = ["id"]



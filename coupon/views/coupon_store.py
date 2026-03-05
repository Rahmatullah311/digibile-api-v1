from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from coupon.models.coupon_store import CouponStore
from rest_framework.permissions import IsAuthenticated
from ..serializers.coupon_store_serializer import (
    CouponStoreCreateSerializer,
    CouponStoreDetailsSerializer,
)
from rest_framework import serializers


class CouponStoreListCreateView(ListCreateAPIView):
    queryset = CouponStore.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        coupon_id = request.data.get("coupon")
        store_id = request.data.get("store_id")

        coupon = CouponStore.objects.get(id=coupon_id) if coupon_id else None
        store = CouponStore.objects.get(id=store_id) if store_id else None

        if not coupon:
            raise serializers.ValidationError("Coupon not found.")

        if not store:
            raise serializers.ValidationError("Store not found.")

        if CouponStore.objects.filter(coupon=coupon, store=store).exists():
            raise serializers.ValidationError(
                "This store is already associated with the coupon."
            )

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CouponStoreCreateSerializer
        return CouponStoreDetailsSerializer


class CouponStoreRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CouponStore.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CouponStoreCreateSerializer
        return CouponStoreDetailsSerializer

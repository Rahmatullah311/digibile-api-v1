from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from coupon.models.coupon_category import CouponCategory
from rest_framework.permissions import IsAuthenticated
from ..serializers.coupon_category_serializer import (
    CouponCategoryCreateSerializer,
    CouponCategoryDetailSerializer,
)
from rest_framework import serializers


class CouponCategoryListCreateView(ListCreateAPIView):
    queryset = CouponCategory.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        coupon_id = request.data.get("coupon")
        category_id = request.data.get("category_id")

        coupon = CouponCategory.objects.get(id=coupon_id) if coupon_id else None
        category = CouponCategory.objects.get(id=category_id) if category_id else None

        if not coupon:
            raise serializers.ValidationError("Coupon not found.")

        if not category:
            raise serializers.ValidationError("Category not found.")

        if CouponCategory.objects.filter(coupon=coupon, category=category).exists():
            raise serializers.ValidationError(
                "This category is already associated with the coupon."
            )

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CouponCategoryCreateSerializer
        return CouponCategoryDetailSerializer


class CouponCategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CouponCategory.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CouponCategoryCreateSerializer
        return CouponCategoryDetailSerializer

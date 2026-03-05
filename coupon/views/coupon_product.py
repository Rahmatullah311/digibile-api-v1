from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from coupon.models.coupon_product import CouponProduct
from rest_framework.permissions import IsAuthenticated
from ..serializers.coupon_product_serializer import (
    CouponProductCreateSerializer,
    CouponProductDetailSerializer,
)
from rest_framework.response import Response
from coupon.models import Coupon
from product.models.product import Product
from rest_framework import serializers


class CouponProductListCreateView(ListCreateAPIView):
    queryset = CouponProduct.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        coupon_id = request.data.get("coupon")
        product_id = request.data.get("product_id")

        coupon = Coupon.objects.get(id=coupon_id) if coupon_id else None
        product = Product.objects.get(id=product_id) if product_id else None

        if not coupon:
            raise serializers.ValidationError("Coupon not found.")

        if not product:
            raise serializers.ValidationError("Product not found.")

        if CouponProduct.objects.filter(coupon=coupon, product=product).exists():
            raise serializers.ValidationError(
                "This product is already associated with the coupon."
            )

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CouponProductCreateSerializer
        return CouponProductDetailSerializer


class CouponProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CouponProduct.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CouponProductCreateSerializer
        return CouponProductDetailSerializer

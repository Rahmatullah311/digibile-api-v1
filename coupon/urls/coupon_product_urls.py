from ..views import (
    CouponProductListCreateView,
    CouponProductRetrieveUpdateDestroyView,
)
from django.urls import path

urlpatterns = [
    path(
        "<int:coupon_id>/products/",
        CouponProductListCreateView.as_view(),
        name="coupon-product-list-create",
    ),
    path(
        "product/<int:pk>/",
        CouponProductRetrieveUpdateDestroyView.as_view(),
        name="coupon-product-detail",
    ),
]

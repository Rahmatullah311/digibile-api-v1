from django.urls import path, include
from coupon.views import (
    CouponListCreateView,
    CouponRetrieveUpdateDestroyView,
)


urlpatterns = [
    path("", CouponListCreateView.as_view(), name="coupon-list-create"),
    path(
        "<int:pk>/",
        CouponRetrieveUpdateDestroyView.as_view(),
        name="coupon-detail",
    ),
    path(
        "",
        include("coupon.urls.coupon_product_urls"),
    ),
    path(
        "",
        include("coupon.urls.coupon_category_urls"),
    ),
    path(
        "",
        include("coupon.urls.coupon_store_urls"),
    ),
]

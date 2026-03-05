from coupon.views.coupon_store import (
    CouponStoreListCreateView,
    CouponStoreRetrieveUpdateDestroyView,
)
from django.urls import path

urlpatterns = [
    path(
        "<int:coupon_id>/stores/",
        CouponStoreListCreateView.as_view(),
        name="coupon-store-list-create",
    ),
    path(
        "store/<int:pk>/",
        CouponStoreRetrieveUpdateDestroyView.as_view(),
        name="coupon-store-detail",
    ),
]

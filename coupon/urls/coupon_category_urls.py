from coupon.views.coupon_category import (
    CouponCategoryListCreateView,
    CouponCategoryRetrieveUpdateDestroyView,
)
from django.urls import path


urlpatterns = [
    path(
        "<int:coupon_id>/categories/",
        CouponCategoryListCreateView.as_view(),
        name="coupon-category-list-create",
    ),
    path(
        "category/<int:pk>/",
        CouponCategoryRetrieveUpdateDestroyView.as_view(),
        name="coupon-category-detail",
    ),
]

from django.urls import path
from product.views.product_views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products-list-create"),
    path(
        "<int:id>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-detail",
    ),
]

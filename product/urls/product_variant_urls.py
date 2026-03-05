from django.urls import path
from product.views.product_variant_views import (
    ProductVariantListCreateView,
)

urlpatterns = [
    path(
        "<int:product_id>/variants/",
        ProductVariantListCreateView.as_view(),
        name="product-variant-list-create",
    ),
]

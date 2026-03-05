from django.urls import path
from product.views.product_attribute_views import (
    ProductAttributeListView,
    ProductAttributeValueListCreateView,
)


urlpatterns = [
    path(
        "attributes/", ProductAttributeListView.as_view(), name="product-attribute-list"
    ),
    path(
        "attribute-values/<int:attribute_id>/",
        ProductAttributeValueListCreateView.as_view(),
        name="product-attribute-value-list-create",
    ),
]

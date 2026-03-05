from django.urls import path
from product.views.product_image_views import (
    ProductImageListCreateAPIView,
    ProductImageRetrieveUpdateDestroyAPIView
)



urlpatterns = [
    path(
        "<int:pk>/images/",
        ProductImageListCreateAPIView.as_view(),
        name="product-images",
    ),
    path(
        "<int:pk>/images/<int:image_id>/",
        ProductImageRetrieveUpdateDestroyAPIView.as_view(),
        name="product-image-detail",
    ),
]

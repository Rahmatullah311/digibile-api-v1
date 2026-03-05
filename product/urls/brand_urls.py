from django.urls import path
from product.views.brand_views import (
    BrandListCreateView,
    BrandRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:brand_id>/', BrandRetrieveUpdateDestroyView.as_view(), name='brand-detail'),
]
from django.urls import path
from product.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path(
        "categories/<int:id>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
]

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer
from core.paginations import CustomPagination


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    pagination_class = CustomPagination



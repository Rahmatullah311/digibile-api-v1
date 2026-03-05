from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from product.models.brand import Brand
from product.serializers.brand_serializer import BrandSerializer
from core.paginations import CustomPagination
from product.filters.brand_filters import BrandFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = []
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = BrandFilter
    ordering = ["-id"]


class BrandRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = []
    lookup_field = "id"
    lookup_url_kwarg = "brand_id"

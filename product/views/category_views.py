from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer
from core.paginations import CustomPagination
from PIL import Image


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = CustomPagination


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"
    pagination_class = CustomPagination

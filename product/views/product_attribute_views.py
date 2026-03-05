from rest_framework.generics import ListCreateAPIView
from product.serializers.attribute_serializer import (
    DetailedAttributeSerializer,
    AttributeValueSerializer,
)
from product.models.attribute import Attribute, AttributeValue
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.paginations import CustomPagination


class ProductAttributeListView(ListCreateAPIView):
    serializer_class = DetailedAttributeSerializer
    queryset = Attribute.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductAttributeValueListCreateView(ListCreateAPIView):
    serializer_class = AttributeValueSerializer
    queryset = AttributeValue.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        attribute_id = self.kwargs.get("attribute_id")
        return AttributeValue.objects.filter(attribute=attribute_id)

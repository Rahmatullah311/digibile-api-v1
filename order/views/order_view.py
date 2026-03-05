from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from order.models.order import Order, OrderItem, OrderItemAttribute
from order.serializers.order_serializer import OrderSerializer, OrderCreateSerializer
from core.paginations import CustomPagination


class OrderListView(ListAPIView):
    queryset = (
        Order.objects.all()
        .select_related("buyer", "store")
        .prefetch_related(
            "items__product", "items__selected_attributes__attribute_value"
        )
    )
    serializer_class = OrderSerializer
    pagination_class = CustomPagination


class OrderDetailView(RetrieveAPIView):
    queryset = (
        Order.objects.all()
        .select_related("buyer", "store")
        .prefetch_related(
            "items__product", "items__selected_attributes__attribute_value"
        )
    )
    serializer_class = OrderSerializer
    lookup_field = "id"
    lookup_url_kwarg = "order_id"


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

from django.urls import path
from order.views.order_view import OrderListView, OrderDetailView, OrderCreateView


urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
]

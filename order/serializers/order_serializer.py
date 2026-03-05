from rest_framework import serializers
from order.models.order import Order, OrderItem, OrderItemAttribute
from product.serializers.attribute_serializer import AttributeValueSerializer
from product.serializers.product_serializer import ProductSerializer
from tokenshield.serializers import UserSerializer
from store.serializers.store_serializer import StoreSerializer
from rest_framework.exceptions import ValidationError
from product.models.attribute import AttributeValue

# -------------------------
# READ SERIALIZERS
# -------------------------


class OrderItemAttributeSerializer(serializers.ModelSerializer):
    """Read-only serializer for OrderItemAttribute, expands AttributeValue."""

    attribute_value = AttributeValueSerializer(read_only=True)

    class Meta:
        model = OrderItemAttribute
        fields = ["id", "attribute_value"]


class OrderItemSerializer(serializers.ModelSerializer):
    """Read-only serializer for OrderItem with product + attributes."""

    selected_attributes = OrderItemAttributeSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "quantity",
            "price",
            "subtotal",
            "selected_attributes",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Read-only serializer for Order with nested buyer, store, and items."""

    buyer = UserSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "store",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]


# -------------------------
# WRITE SERIALIZERS (CREATE)
# -------------------------


class OrderItemAttributeCreateSerializer(serializers.ModelSerializer):
    attribute_value = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all()
    )

    class Meta:
        model = OrderItemAttribute
        fields = ["attribute_value"]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    selected_attributes = OrderItemAttributeCreateSerializer(many=True, write_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price", "selected_attributes"]

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        price = data["price"]

        # 1. Quantity must be > 0
        if quantity <= 0:
            raise ValidationError({"quantity": "Quantity must be greater than 0."})

        # 2. Price must match product price
        if product.price != price:
            raise ValidationError(
                {"price": f"Price mismatch. Expected {product.price}."}
            )

        return data


class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "buyer",
            "status",
            "total_amount",
            "created_date",
        ]

    def validate(self, data):
        store = data["store"]
        items = data["items"]

        # print("validated_data: ", data)

        for item in items:
            product = item["product"]
            # 3. Ensure product belongs to the store
            if product.store_id != store.id:
                raise ValidationError(
                    {
                        "store": f"Product {product.id} does not belong to store {store.id}."
                    }
                )
            selected_attributes = item["selected_attributes"]

            for attribute in selected_attributes:
                print("attribute_value: ", attribute["attribute_value"])

        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            attributes_data = item_data.pop("selected_attributes", [])
            order_item = OrderItem.objects.create(order=order, **item_data)
            for attr_data in attributes_data:
                OrderItemAttribute.objects.create(order_item=order_item, **attr_data)

        order.calculate_total()

        return order

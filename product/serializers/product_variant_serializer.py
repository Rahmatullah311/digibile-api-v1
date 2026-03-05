from rest_framework import serializers
from product.models.attribute import AttributeValue
from product.models.product_variant import ProductVariant
from product.serializers.attribute_serializer import (
    AttributeValueSerializer,
)
import json


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all(), many=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "sku",
            "price",
            "stock",
            "is_active",
            "created_at",
            "created_by",
            "attributes",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["attributes"] = AttributeValueSerializer(
            instance.attributes.all(), many=True
        ).data
        return rep

    def to_internal_value(self, data):
        # If attributes is a string like "[1,2,3]", parse it
        attrs = data.get("attributes")
        if isinstance(attrs, str):
            try:
                parsed = json.loads(attrs)
                if isinstance(parsed, list):
                    data = data.copy()
                    data.setlist("attributes", parsed)
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    {"attributes": "Must be a valid list or JSON array"}
                )
        return super().to_internal_value(data)

    def create(self, validated_data):
        attributes_data = validated_data.pop("attributes", [])
        product_variant = ProductVariant.objects.create(**validated_data)
        product_variant.attributes.set(attributes_data)
        return product_variant

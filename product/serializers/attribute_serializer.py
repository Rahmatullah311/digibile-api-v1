from rest_framework import serializers
from product.models.attribute import Attribute, AttributeValue


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "name", "slug"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only = True)
    attribute_id = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all(),
        source="attribute",
        write_only=True
    )


    class Meta:
        model = AttributeValue
        fields = ["id", "value", "attribute", "attribute_id"]


class DetailedAttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ["id", "name", "slug", "values"]

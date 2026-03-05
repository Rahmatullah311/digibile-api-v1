from rest_framework import serializers
from product.models.product import Product
from store.serializers import StoreSerializer
from product.serializers.category_serializer import CategorySerializer
from product.serializers.brand_serializer import BrandSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField
from product.serializers.product_image_serializer import ProductImageSerializer
from product.serializers.product_variant_serializer import ProductVariantSerializer


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=StoreSerializer.Meta.model.objects.all(),
        source="store",
        write_only=True,
    )
    store = StoreSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    tags = TagListSerializerField()
    created_by = serializers.ReadOnlyField(source="created_by.username")
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            "id",
            "store",
            "store_id",
            "name",
            "slug",
            "category",
            "brand",
            "description",
            "short_description",
            "price",
            "old_price",
            "stock",
            "is_featured",
            "is_digital",
            "status",
            "tags",
            "images",
            "variants",
            "seo_title",
            "seo_description",
            "available_from",
            "available_to",
            "created_at",
            "created_by",
        )
        read_only_fields = ("id", "store", "created_at", "created_by")

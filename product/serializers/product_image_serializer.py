from rest_framework import serializers
from product.models.product_image import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]


class ProductImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    alt_texts = serializers.ListField(
        child=serializers.CharField(max_length=255, allow_blank=True),
        write_only=True,
        required=False,
    )

    def validate(self, data):
        alt_texts = data.get("alt_texts", [])
        images = data["images"]

        if alt_texts and len(alt_texts) != len(images):
            raise serializers.ValidationError(
                "alt_texts count must match images count."
            )
        return data

    def create(self, validated_data):
        product = self.context["product"]  # Passed from view
        images = validated_data["images"]
        alt_texts = validated_data.get("alt_texts", [""] * len(images))

        image_objects = []
        for img, alt in zip(images, alt_texts):
            image_objects.append(ProductImage(product=product, image=img, alt_text=alt))

        return ProductImage.objects.bulk_create(image_objects)

# product/serializers/category_serializer.py
from rest_framework import serializers
from product.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    # writable field for upload
    image = serializers.ImageField(required=False, allow_null=True, write_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        # include 'image' so DRF accepts file uploads
        fields = ["id", "name", "slug", "parent", "image", "image_url", "thumbnail_url"]
        read_only_fields = ["id", "image_url", "thumbnail_url"]

    def _abs(self, url):
        request = self.context.get("request")
        if not url:
            return None
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_image_url(self, obj):
        return self._abs(obj.image.url) if obj.image else None

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self._abs(obj.thumbnail.url)
        if obj.image:
            return self._abs(obj.image.url)
        return None

    def create(self, validated_data):
        # Pop image out and attach after instance creation so slug exists
        image = validated_data.pop("image", None)
        category = Category.objects.create(**validated_data)
        if image:
            # save file to field (this will trigger model.save(), and thumbnail generation)
            category.image.save(image.name, image, save=True)
        return category

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Save other fields first (so slug, etc)
        instance.save()
        if image is not None:
            # replace image; model.save() will detect change and create thumbnail
            instance.image.save(image.name, image, save=True)
        return instance

from rest_framework import serializers
from product.models.brand import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo", "thumbnail"]

    def _abs(self, url):
        request = self.context.get("request")
        if not url:
            return None
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_logo_url(self, obj):
        return self._abs(obj.logo.url) if obj.logo else None

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self._abs(obj.thumbnail.url)
        if obj.logo:
            return self._abs(obj.logo.url)
        return None

    def create(self, validated_data):
        logo = validated_data.pop("logo", None)
        brand = Brand.objects.create(**validated_data)
        if logo:
            brand.logo.save(logo.name, logo, save=True)
        return brand

    def update(self, instance, validated_data):
        logo = validated_data.pop("logo", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if logo is not None:
            instance.logo.save(logo.name, logo, save=True)
        return instance

from rest_framework import serializers
from tokenshield.serializers import UserSerializer
from ..models import Store


class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source="owner",
        write_only=True,
        required=True,
    )

    # Allow nullable file fields
    logo = serializers.ImageField(required=False, allow_null=True)
    banner = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Store
        fields = [
            "id",
            "owner_id",
            "owner",
            "name",
            "slug",
            "description",
            "logo",
            "logo_thumbnail",
            "banner",
            "email",
            "email_verified",
            "phone",
            "phone_verified",
            "website",
            "address",
            "facebook",
            "instagram",
            "twitter",
            "status",
            "is_featured",
            "seo_title",
            "seo_description",
            "verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "logo_thumbnail"]

    def create(self, validated_data):
        # Handle missing logo safely
        if "logo" not in validated_data or validated_data["logo"] in (None, ""):
            validated_data["logo"] = None
        if "banner" not in validated_data or validated_data["banner"] in (None, ""):
            validated_data["banner"] = None

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle null logo/banner on update
        if "logo" in validated_data and validated_data["logo"] in (None, ""):
            validated_data["logo"] = None
        if "banner" in validated_data and validated_data["banner"] in (None, ""):
            validated_data["banner"] = None

        return super().update(instance, validated_data)

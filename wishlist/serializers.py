from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Wishlist, WishlistItem
import difflib


class WishlistSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    items_count = serializers.IntegerField(
        source="wishlist_items.count", read_only=True
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "items_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]

    def validate(self, attrs):
        """Ensure the wishlist name is unique (and not too similar) for the owner."""
        request = self.context.get("request")
        owner = request.user if request else None
        name = attrs.get("name")

        # If name isn't being provided (partial update), skip validation here.
        if not name:
            return attrs

        name_norm = name.strip().lower()

        # Exclude the instance itself when updating
        qs = Wishlist.objects.filter(owner=owner)
        if getattr(self, "instance", None):
            qs = qs.exclude(pk=self.instance.pk)

        # Exact (case-insensitive) duplicate check
        if qs.filter(name__iexact=name).exists():
            raise serializers.ValidationError(
                "You already have a wishlist with this name."
            )

        # Similarity check: prevent names that are too close (e.g. typos)

        SIMILARITY_THRESHOLD = 0.85  # tune as needed (0..1)
        for existing_name in qs.values_list("name", flat=True):
            if (
                difflib.SequenceMatcher(
                    None, name_norm, (existing_name or "").strip().lower()
                ).ratio()
                >= SIMILARITY_THRESHOLD
            ):
                raise serializers.ValidationError(
                    "A wishlist with a very similar name already exists."
                )

        return attrs


class WishlistItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.SlugRelatedField(
        slug_field="model", queryset=ContentType.objects.all()
    )
    content_object_repr = serializers.SerializerMethodField()
    wishlist = serializers.PrimaryKeyRelatedField(queryset=Wishlist.objects.all())

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "wishlist",
            "user",
            "content_type",
            "object_id",
            "content_object_repr",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        """Ensure the combination of user, content_type, and object_id is unique."""
        request = self.context.get("request")
        user = request.user if request else None
        content_type = attrs.get("content_type")
        object_id = attrs.get("object_id")

        if WishlistItem.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        ).exists():
            raise serializers.ValidationError("This item is already in your wishlist.")
        return attrs

    def get_content_object_repr(self, obj):
        """Return string representation of the related object."""
        try:
            return str(obj.content_object)
        except Exception:
            return None

    def create(self, validated_data):
        """Automatically assign the current user when creating."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):

            validated_data["user"] = request.user
        return super().create(validated_data)

from rest_framework import serializers
from tokenshield.serializers import UserSerializer
from store.models import StoreStaff


class StoreStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    store = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StoreStaff
        fields = [
            "id",
            "store",
            "user",
            "role",
            "is_active",
            "joined_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        depth = 1

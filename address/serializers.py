# addresses/serializers.py
from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "user_email",
            "title",
            "reciever_name",
            "phone",
            "address_type",
            "address_line1",
            "address_line2",
            "street",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "is_default",
        ]
        read_only_fields = ["user_email"]

# tokenshield/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from address.serializers import AddressSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        serializer = UserSerializer(user, context=self.context)
        data["user"] = serializer.data
        data["permissions"] = list(user.get_all_permissions())

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,  # 🔴 important: allows update without password
        min_length=8,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
        label="Confirm Password",
    )
    addresses = AddressSerializer(many=True, read_only=True)

    avatar = serializers.ImageField(required=False, allow_null=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "email_verified",
            "phone",
            "phone_verified",
            "first_name",
            "last_name",
            # 🖼️ avatar
            "avatar",
            "avatar_thumbnail",
            # 📍 address
            "country",
            "state",
            "city",
            "address",
            "zip_code",
            # 🔐 auth / status
            "password",
            "password2",
            "is_active",
            "status",
            "is_staff",
            "last_login",
            "date_joined",
            "addresses",
        ]
        read_only_fields = [
            "email_verified",
            "avatar_thumbnail",
            "is_active",
            "is_staff",
            "last_login",
            "date_joined",
            "addresses",
        ]

    def validate_email(self, value):
        if self.instance is None and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password or password2:
            if password != password2:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."}
                )
            validate_password(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)

        password = validated_data.pop("password", None)

        user = User.objects.create_user(
            email=validated_data["email"],
            password=password,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            **{
                k: v
                for k, v in validated_data.items()
                if k not in ["email", "first_name", "last_name"]
            },
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserRegisterSerializer(UserSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        self._refresh = RefreshToken.for_user(user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh = getattr(self, "_refresh", None)

        if refresh:
            return {
                "user": data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        return data


class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "is_superuser",
            "email",
            "email_verified",
            "phone",
            "phone_verified",
            "first_name",
            "last_name",
            # 🖼️ avatar
            "avatar",
            "avatar_thumbnail",
            # 📍 address
            "country",
            "state",
            "city",
            "address",
            "zip_code",
            "is_active",
            "status",
            "is_staff",
            "last_login",
            "date_joined",
        ]

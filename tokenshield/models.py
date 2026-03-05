from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def upload_to(instance, filename):
    return f"users/avatars/{instance.id}.webp"


def thumbnail_upload_to(instance, filename):
    return f"users/avatars/thumbnails/{instance.id}_thumb.webp"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("rejected", "Rejected"),
        ("banned", "Banned"),
    ]

    username = None
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    avatar_thumbnail = models.ImageField(
        upload_to=thumbnail_upload_to, null=True, blank=True
    )

    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=16, choices=USER_STATUS_CHOICES, default="active"
    )
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Save first to get user ID
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.avatar:
            self._process_avatar()

    def _process_avatar(self):
        """Convert avatar to WEBP and generate thumbnail"""

        img = Image.open(self.avatar)
        img = img.convert("RGB")

        # ----- MAIN AVATAR -----
        avatar_io = BytesIO()
        img.save(avatar_io, format="WEBP", quality=85)
        avatar_name = f"{self.id}.webp"

        self.avatar.save(
            avatar_name,
            ContentFile(avatar_io.getvalue()),
            save=False,
        )

        # ----- THUMBNAIL -----
        thumb_size = (200, 200)
        thumb = img.copy()
        thumb.thumbnail(thumb_size)

        thumb_io = BytesIO()
        thumb.save(thumb_io, format="WEBP", quality=80)
        thumb_name = f"{self.id}_thumb.webp"

        self.avatar_thumbnail.save(
            thumb_name,
            ContentFile(thumb_io.getvalue()),
            save=False,
        )

        super().save(update_fields=["avatar", "avatar_thumbnail"])
    
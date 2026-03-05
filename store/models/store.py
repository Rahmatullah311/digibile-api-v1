from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

User = get_user_model()


def upload_to(instance, filename):
    # Use instance.pk or generate a temporary name
    if instance.pk:
        return f"stores/logos/{instance.pk}.webp"
    else:
        # Generate a temporary name - will be renamed after save
        import uuid

        return f"stores/logos/temp_{uuid.uuid4().hex}.webp"


def thumbnail_upload_to(instance, filename):
    if instance.pk:
        return f"stores/logos/thumbnails/{instance.pk}_thumb.webp"
    else:
        import uuid

        return f"stores/logos/thumbnails/temp_{uuid.uuid4().hex}_thumb.webp"


class Store(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("rejected", "Rejected"),
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_stores"
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    logo_thumbnail = models.ImageField(
        upload_to=thumbnail_upload_to, null=True, blank=True
    )
    banner = models.ImageField(upload_to="stores/banners/", blank=True, null=True)

    email = models.EmailField(blank=True)
    email_verified = models.BooleanField(default=False, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    phone_verified = models.BooleanField(default=False, null=True, blank=True)
    website = models.URLField(blank=True)

    address = models.TextField(blank=True)

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_featured = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    verified = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate slug if not exists
        if not self.slug:
            self.slug = slugify(self.name)

        # First save to get an ID
        super().save(*args, **kwargs)

        # Process logo if it exists
        if self.logo:
            self._process_logo()

    def _process_logo(self):
        """Convert logo to WEBP and generate thumbnail"""
        try:
            img = Image.open(self.logo)
            img = img.convert("RGB")

            # Process main logo
            logo_io = BytesIO()
            img.save(logo_io, format="WEBP", quality=85)
            logo_content = ContentFile(logo_io.getvalue())

            # Generate new filename with actual ID
            logo_name = f"{self.id}.webp"

            # Save the new file
            self.logo.save(logo_name, logo_content, save=False)

            # Process thumbnail
            thumb_size = (200, 200)
            thumb = img.copy()
            thumb.thumbnail(thumb_size)

            thumb_io = BytesIO()
            thumb.save(thumb_io, format="WEBP", quality=80)
            thumb_content = ContentFile(thumb_io.getvalue())

            thumb_name = f"{self.id}_thumb.webp"
            self.logo_thumbnail.save(thumb_name, thumb_content, save=False)

            # Save without triggering save() again to avoid recursion
            super().save(update_fields=["logo", "logo_thumbnail"])

        except Exception as e:
            # Log the error but don't break the save
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error processing logo for store {self.id}: {e}")

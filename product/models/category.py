from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

def upload_to(instance, filename):
    return f"category/{instance.slug}.webp"

def thumbnail_upload_to(instance, filename):
    return f"category/thumbnails/{instance.slug}_thumb.webp"


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    # Always store as WebP
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Track previous file names
        old_image = None
        old_thumb = None
        if self.pk:
            try:
                old = Category.objects.get(pk=self.pk)
                old_image = old.image.name
                old_thumb = old.thumbnail.name
            except Category.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # No image uploaded
        if not self.image:
            return

        # Always convert and regenerate
        self._process_image()
        self._generate_thumbnail()

        # Save only these fields to prevent recursion
        super().save(update_fields=["image", "thumbnail"])

        # Remove old files
        self._delete_old_file(old_image, self.image.name)
        self._delete_old_file(old_thumb, self.thumbnail.name)

    # ------------------------ INTERNAL HELPERS ------------------------

    def _open_image(self):
        """Open image safely using file storage."""
        try:
            return Image.open(self.image.open("rb"))
        except:
            return Image.open(self.image.path)

    def _process_image(self):
        """Convert uploaded image to WebP."""
        img = self._open_image()

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=85)
        buffer.seek(0)

        filename = f"{self.slug}.webp"
        self.image.save(filename, ContentFile(buffer.read()), save=False)

    def _generate_thumbnail(self, size=(300, 300)):
        """Create and save a WebP thumbnail."""
        img = self._open_image()

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(size, Image.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=70)
        buffer.seek(0)

        filename = f"{self.slug}_thumb.webp"
        self.thumbnail.save(filename, ContentFile(buffer.read()), save=False)

    def _delete_old_file(self, old_name, new_name):
        """Remove old file if replaced."""
        if old_name and old_name != new_name:
            try:
                storage = self.image.storage
                if storage.exists(old_name):
                    storage.delete(old_name)
            except Exception:
                pass

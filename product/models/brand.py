from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def upload_to(instance, filename):
    return f"brand/{instance.slug}.webp"


def thumbname_upload_to(instance, filename):
    return f"brand/thumbnails/{instance.slug}_thumb.webp"


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=thumbname_upload_to, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Track previous file names
        old_logo = None
        old_thumb = None
        if self.pk:
            try:
                old = Brand.objects.get(pk=self.pk)
                old_logo = old.logo.name
                old_thumb = old.thumbnail.name
            except Brand.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # No logo uploaded
        if not self.logo:
            return

        # Always convert and regenerate
        self._process_logo()
        self._generate_thumbnail()

        # Save only these fields to prevent recursion
        super().save(update_fields=["logo", "thumbnail"])

        # Remove old files
        self._delete_old_file(old_logo, self.logo.name)
        self._delete_old_file(old_thumb, self.thumbnail.name)

    def _open_logo(self):
        """Open logo safely using file storage."""
        try:
            return Image.open(self.logo.open("rb"))
        except:
            return Image.open(self.logo.path)

    def _process_logo(self):
        """Convert uploaded image to WebP."""
        logo = self._open_logo()

        if logo.mode in ("RGBA", "P"):
            logo = logo.convert("RGB")

        buffer = BytesIO()
        logo.save(buffer, format="WEBP", quality=85)
        buffer.seek(0)

        filename = f"{self.slug}.webp"
        self.logo.save(filename, ContentFile(buffer.read()), save=False)

    def _generate_thumbnail(self, size=(300, 300)):
        """Create and save a WebP thumbnail."""
        logo = self._open_logo()

        if logo.mode in ("RGBA", "P"):
            logo = logo.convert("RGB")

        logo.thumbnail(size, Image.LANCZOS)

        buffer = BytesIO()
        logo.save(buffer, format="WEBP", quality=70)
        buffer.seek(0)

        filename = f"{self.slug}_thumb.webp"
        self.thumbnail.save(filename, ContentFile(buffer.read()), save=False)

    def _delete_old_file(self, old_name, new_name):
        """Remove old file if replaced."""
        if old_name and old_name != new_name:
            try:
                storage = self.logo.storage
                if storage.exists(old_name):
                    storage.delete(old_name)
            except Exception:
                pass

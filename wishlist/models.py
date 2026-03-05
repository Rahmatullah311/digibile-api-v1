from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


user = get_user_model()


class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(user, related_name="wishlists", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, related_name="wishlist_items", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        user, related_name="wishlist_items", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="The content type of the wishlisted item.",
    )
    object_id = models.PositiveIntegerField(help_text="The ID of the wishlisted item.")
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.content_object}"

from django.contrib import admin
from .models import Wishlist, WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "owner__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content_type", "object_id", "created_at")
    list_filter = ("created_at", "content_type")
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

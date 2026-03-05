# addresses/admin.py
from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user_email",
        "address_type",
        "city",
        "state",
        "country",
        "is_default",
    )
    list_filter = ("address_type", "country", "is_default")
    search_fields = ("user__email", "city", "state", "postal_code")

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = "user__email"  # Allows sorting by user email
    user_email.short_description = "User Email"

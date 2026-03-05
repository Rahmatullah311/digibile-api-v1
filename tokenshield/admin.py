# tokenshield/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "phone", "first_name", "last_name", "is_staff")
    ordering = ("email",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "email_verified",
                    "phone",
                    "phone_verified",
                    "password",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "status",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),  # removed `date_joined`
    )

    readonly_fields = ("last_login", "date_joined")  # ✅ Add this line

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")

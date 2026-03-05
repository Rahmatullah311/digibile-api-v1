from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StoreStaff(models.Model):
    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("inventory", "Inventory Manager"),
        ("support", "Customer Support"),
    )

    store = models.ForeignKey(
        "Store", on_delete=models.CASCADE, related_name="staff_members"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store_roles")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="manager")
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("store", "user")
        verbose_name = "Store Staff"
        verbose_name_plural = "Store Staff"

    def __str__(self):
        return f"{self.user.username} - {self.role} @ {self.store.name}"

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Coupon(models.Model):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED, "Fixed amount"),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    usage_limit = models.PositiveIntegerField(
        default=0, help_text="Total uses allowed (0 = unlimited)"
    )
    used_count = models.PositiveIntegerField(default=0)

    per_user_limit = models.PositiveIntegerField(
        default=1, help_text="How many times a single user can use it"
    )

    applicable_to_all = models.BooleanField(default=True)
    # Optional: Add relations to specific products or categories
    # products = models.ManyToManyField('shop.Product', blank=True)
    # categories = models.ManyToManyField('shop.Category', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code

    # -----------------------
    # Helper methods
    # -----------------------
    def is_valid(self):
        now = timezone.now()
        return (
            self.active
            and self.valid_from <= now <= self.valid_to
            and (self.usage_limit == 0 or self.used_count < self.usage_limit)
        )

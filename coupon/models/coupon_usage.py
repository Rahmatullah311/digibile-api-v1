from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class CouponUsage(models.Model):
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.CASCADE, related_name="usages"
    )
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="coupon_usages",
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applied_coupons",
    )
    used_at = models.DateTimeField(auto_now_add=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("coupon", "user", "order")
        ordering = ["-used_at"]

    def __str__(self):
        return f"{self.user} used {self.coupon.code} ({self.discount_amount})"

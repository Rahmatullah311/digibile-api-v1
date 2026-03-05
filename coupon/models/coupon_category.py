from django.db import models
from coupon.models.coupon import Coupon


class CouponCategory(models.Model):
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="coupon_categories"
    )
    category = models.ForeignKey(
        "product.Category", on_delete=models.CASCADE, related_name="category_coupons"
    )

    class Meta:
        unique_together = ("coupon", "category")
        verbose_name = "Coupon Category"
        verbose_name_plural = "Coupon Categories"

    def __str__(self):
        return f"{self.coupon.code} → {self.category.name}"

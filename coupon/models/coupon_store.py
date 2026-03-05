from django.db import models
from coupon.models.coupon import Coupon


class CouponStore(models.Model):
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="coupon_stores"
    )
    store = models.ForeignKey(
        "store.Store", on_delete=models.CASCADE, related_name="store_coupons"
    )

    class Meta:
        unique_together = ("coupon", "store")
        verbose_name = "Coupon Store"
        verbose_name_plural = "Coupon Stores"

    def __str__(self):
        return f"{self.coupon.code} → {self.store.name}"

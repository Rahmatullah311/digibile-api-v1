from django.db import models
from coupon.models.coupon import Coupon


class CouponProduct(models.Model):
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="coupon_products"
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="product_coupons"
    )

    class Meta:
        unique_together = ("coupon", "product")
        verbose_name = "Coupon Product"
        verbose_name_plural = "Coupon Products"

    def __str__(self):
        return f"{self.coupon.code} → {self.product.name}"

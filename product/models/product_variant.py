from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class ProductVariant(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="product_variants"
    )
    attributes = models.ManyToManyField("AttributeValue", related_name="variants")

    def __str__(self):
        attr_values = ", ".join([str(val) for val in self.attributes.all()])
        return f"{self.product.name} ({attr_values})"

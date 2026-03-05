from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    store = models.ForeignKey(
        "store.Store", on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount"])
        return total

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.last_name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "product.Product", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # snapshot at order time
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        attrs = ", ".join([str(attr) for attr in self.selected_attributes.all()])
        return f"{self.quantity} x {self.product.name} ({attrs})"


class OrderItemAttribute(models.Model):
    """
    Stores the chosen attribute values per OrderItem.
    (e.g., Color=Black, Size=XL, Storage=128GB).
    """

    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="selected_attributes"
    )
    attribute_value = models.ForeignKey(
        "product.AttributeValue", on_delete=models.PROTECT
    )

    def __str__(self):
        return str(self.attribute_value)

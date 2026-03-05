from django.db import models


# Create your models here.
class Address(models.Model):

    ADDRESS_TYPE_CHOICES = [("shipping", "Shipping"), ("billing", "Billing")]
    user = models.ForeignKey(
        "tokenshield.User", related_name="addresses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=20)
    reciever_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    # map coordinates
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_type} address for {self.user.email}"

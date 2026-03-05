from django.db import models
from taggit.managers import TaggableManager


class Product(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    store = models.ForeignKey(
        "store.Store", on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
    )
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField()
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    tags = TaggableManager()
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

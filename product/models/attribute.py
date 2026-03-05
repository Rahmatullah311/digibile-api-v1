from django.db import models


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

from django.contrib import admin
from product.models.product import Product
from product.models.attribute import Attribute, AttributeValue
from product.models.brand import Brand
from product.models.category import Category
from product.models.product_image import ProductImage
from product.models.product_variant import ProductVariant

admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(Product)

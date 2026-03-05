from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/tokenshield/", include("tokenshield.urls")),
    path("api/product/", include("product.urls.product_urls")),
    path("api/product/", include("product.urls.product_image_urls")),
    path("api/product/", include("product.urls.product_variant_urls")),
    path("api/category/", include("product.urls.category_urls")),
    path("api/product/", include("product.urls.product_attribute_urls")),
    path("api/brand/", include("product.urls.brand_urls")),
    path("api/store/", include("store.urls.store_urls")),
    path("api/store/<int:store_id>/staff/", include("store.urls.store_staff_urls")),
    path("api/order/", include("order.urls.order_urls")),
    path("api/address/", include("address.urls")),
    path("api/ticket/", include("ticket.urls")),
    path("api/wishlist/", include("wishlist.urls.wishlist_urls")),
    path("api/wishlist/", include("wishlist.urls.wishlist_item_urls")),
    path("api/coupon/", include("coupon.urls.coupon_url")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
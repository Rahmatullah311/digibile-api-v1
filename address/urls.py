# addresses/urls.py
from django.urls import path
from .views import (
    UserAddressListCreateView,
    UserAddressDetailView,
    AdminAddressSearchView,
    UserAddressAPIView,
    ChangeUserDefaultAddressAPIView,
)

urlpatterns = [
    path("my-addresses/", UserAddressListCreateView.as_view(), name="my-addresses"),
    path(
        "my-addresses/<int:pk>/", UserAddressDetailView.as_view(), name="address-detail"
    ),
    path(
        "admin/search-addresses/",
        AdminAddressSearchView.as_view(),
        name="admin-search-addresses",
    ),
    path(
        "addresses/<int:user>/addresses",
        UserAddressAPIView.as_view(),
        name="user-addresses",
    ),
    path(
        "addresses/<int:user>/change_default_address/<int:address>",
        ChangeUserDefaultAddressAPIView.as_view(),
        name="change_default_address",
    ),
]

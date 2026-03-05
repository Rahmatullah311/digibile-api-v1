from django.urls import path
from store.views.store_staff_views import (
    StoreStaffListCreateView,
    StoreStaffRetrieveUpdateDestroyView,
)


urlpatterns = [
    path(
        "",
        StoreStaffListCreateView.as_view(),
        name="store_staff_list_create",
    ),
    path(
        "<int:pk>/",
        StoreStaffRetrieveUpdateDestroyView.as_view(),
        name="store_staff_detail",
    ),
]

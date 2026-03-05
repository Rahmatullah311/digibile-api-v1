from django.urls import path, include
from store.views.store_views import (
    StoreListCreateView,
    StoreRetrieveUpdateDestroyView,
    StoreCountView,
    AllStoresCount,
)


urlpatterns = [
    path("", StoreListCreateView.as_view(), name="store-list-create"),
    path(
        "<int:id>/",
        StoreRetrieveUpdateDestroyView.as_view(),
        name="store-retrieve-update-destroy",
    ),
    path("count/", StoreCountView.as_view(), name="store-count"),
    path("count/all/", AllStoresCount.as_view(), name="all-store-count"),
]

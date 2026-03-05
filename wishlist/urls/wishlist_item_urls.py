from django.urls import path
from ..views.wishlist_item import (
    WishListItemListCreateView,
    WishlistItemRetrieveUpdateDestroyView,
)


urlpatterns = [
    path(
        "<int:wishlist_id>/items/",
        WishListItemListCreateView.as_view(),
        name="wishlist-item-list-create",
    ),
    path(
        "items/<int:pk>/",
        WishlistItemRetrieveUpdateDestroyView.as_view(),
        name="wishlist-item-retrieve-update-destroy",
    ),
]

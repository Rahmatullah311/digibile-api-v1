from django.urls import path
from ..views.wishlist import WishlistListCreateView, WishListRetrieveUpdateDestroyView
from ..views.wishlist_item import WishListItemListCreateView


urlpatterns = [
    path("", WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path(
        "<int:pk>/",
        WishListRetrieveUpdateDestroyView.as_view(),
        name="wishlist-detail",
    ),
]

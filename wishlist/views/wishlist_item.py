from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import Wishlist, WishlistItem
from ..serializers import WishlistSerializer, WishlistItemSerializer


class WishListItemListCreateView(ListCreateAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wishlist_id = self.kwargs.get("wishlist_id")
        self.queryset = self.queryset.filter(
            wishlist=wishlist_id, user=self.request.user
        )
        return self.queryset

    def perform_create(self, serializer):
        wishlistId = self.kwargs.get("wishlist_id")
        wishlist = Wishlist.objects.get(id=wishlistId)
        serializer.save(user=self.request.user, wishlist=wishlist)



class WishlistItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return self.queryset
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Address
from .serializers import AddressSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

User = get_user_model()


# ✅ List + Create user’s own addresses
class UserAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Normal users → only their own addresses
        # Admins → all addresses
        if self.request.user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(user=self.request.user)


# ✅ Retrieve + Update + Delete user’s address
class UserAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Address.objects.none()  # no addresses for anonymous
        if user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(user=user)


# ✅ Admin/Staff search by user email
class AdminAddressSearchView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Address.objects.all()
        email = self.request.query_params.get("email")
        if email:
            queryset = queryset.filter(user__email__icontains=email)
        return queryset


class UserAddressAPIView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.kwargs["user"]
        print(f"user Id: {user}")
        queryset = Address.objects.filter(user=user).all()
        return queryset


class ChangeUserDefaultAddressAPIView(APIView):

    def patch(self, request, user, address):

        # 🔐 Security check (important)
        # uncomment this code to enable authenticated user only to change default address
        # if request.user.id != user:
        #     return Response(
        #         {"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        #     )

        # 1️⃣ Remove old default addresses
        Address.objects.filter(user_id=user, is_default=True).update(is_default=False)

        # 2️⃣ Set new default address
        new_default = get_object_or_404(Address, id=address, user_id=user)
        new_default.is_default = True
        new_default.save()

        # 3️⃣ Serialize updated address
        serializer = AddressSerializer(new_default)

        return Response(serializer.data, status=status.HTTP_200_OK)

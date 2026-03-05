from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from store.models import StoreStaff
from store.serializers.store_staff_serializer import StoreStaffSerializer
from django.shortcuts import get_object_or_404
from store.models import Store
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

class StoreStaffListCreateView(ListCreateAPIView):
    serializer_class = StoreStaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store_id = self.kwargs.get("store_id")
        return StoreStaff.objects.filter(store_id=store_id)

    def perform_create(self, serializer):
        # Get store
        store_id = self.kwargs.get("store_id")
        store = get_object_or_404(Store, id=store_id)

        # Get staff (user) by user_id
        staff_id = self.request.data.get("user_id")
        staff = get_object_or_404(get_user_model(), id=staff_id)

        if StoreStaff.objects.filter(store=store, user=staff).exists():
            raise ValidationError({"detail": "This user is already a staff member of this store."})

        try:
            serializer.save(store=store, user=staff)
        except IntegrityError:
            raise ValidationError({"detail": "Could not add staff due to a database constraint."})


class StoreStaffRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = StoreStaff.objects.all()
    serializer_class = StoreStaffSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from store.serializers.store_serializer import StoreSerializer
from store.models import Store
from rest_framework.response import Response
from rest_framework import status
from core.paginations import CustomPagination
from tokenshield.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from store.filters import StoreFilter


class StoreListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer
    pagination_class = CustomPagination
    queryset = Store.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StoreFilter

    filtering_fields = [
        "name",
        "description",
        "email",
        "phone",
        "email_verified",
        "phone_verified",
    ]
    ordering = ["name"]

    # def get_queryset(self):
    #     user_role = self.request.user.is_staff
    #     if user_role:
    #         return Store.objects.all()
    #     return Store.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if self.request.POST["owner_id"]:
            owner_id = self.request.POST["owner_id"]
            owner = User.objects.filter(id=owner_id).first()
            serializer.save(owner=owner)
        else:
            serializer.save(owner=self.request.user)


class StoreRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Store.objects.filter(owner=request.user).count()
        return Response({"store_count": count}, status=status.HTTP_200_OK)


class AllStoresCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Store.objects.all().count()
        return Response({"store_count": count}, status=status.HTTP_200_OK)

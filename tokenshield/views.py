from django.shortcuts import render
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer, UserListSerializer
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from core.paginations import CustomPagination
from rest_framework.generics import DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import UserFilter


# Create your views here.


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserApiView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        loggedInUser = request.user
        serializer = self.get_serializer(loggedInUser)
        userPermissions = request.user.get_all_permissions()

        response = {
            "user": serializer.data,
            "permissions": userPermissions,
        }

        return Response(response)


class UsersListView(ListAPIView):
    model = User
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = UserFilter
    filtering_fields = ["id", "email", "first_name", "date_joined"]
    ordering = ["-id"]


class UserDestroyAPIView(DestroyAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

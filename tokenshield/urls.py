from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from tokenshield.views import (
    RegisterView,
    UserApiView,
    CustomLoginView,
    UsersListView,
    UserDestroyAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)


urlpatterns = [
    path("token/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/register/", RegisterView.as_view(), name="register"),
    path("user/me/", UserApiView.as_view(), name="user_api_view"),
    path("user/all/", UsersListView.as_view(), name="users_list"),
    path("user/<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="users_list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user"),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (
    ChangeEmailView,
    ChangePasswordView,
    LoginView,
    UserViewSet,
)

app_name = "accounts"

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
    path(
        "<slug:username>/change-email/",
        ChangeEmailView.as_view(),
        name="change-email",
    ),
    path(
        "<slug:username>/change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("", include(router.urls)),
]

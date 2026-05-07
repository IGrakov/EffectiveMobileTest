from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (
    ChangeEmailView,
    ChangePasswordView,
    LoginView,
    LogoutView,
    UserViewSet,
)

app_name = "user"

router = SimpleRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
    path(
        "change-email/",
        ChangeEmailView.as_view(),
        name="change-email",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("", include(router.urls)),
]

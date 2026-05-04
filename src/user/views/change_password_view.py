from rest_framework.serializers import BaseSerializer

from user.serializers import ChangePasswordSerializer
from user.views.base_user_change_view import BaseUserChangeView


class ChangePasswordView(BaseUserChangeView):
    serializer_class = ChangePasswordSerializer
    update_field = "password"
    password_check_key = "old_password"  # noqa: S105

    def perform_update(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        user.set_password(
            serializer.validated_data["new_password"],
        )
        user.save()

from user.serializers import ChangeEmailSerializer
from user.views.base_user_change_view import BaseUserChangeView


class ChangeEmailView(BaseUserChangeView):
    serializer_class = ChangeEmailSerializer
    update_field = "email"
    password_check_key = "password"

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView


class BaseUserChangeView(APIView):
    serializer_class: type[BaseSerializer]
    update_field: str
    password_check_key: str

    @extend_schema(
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "example": {"detail": "string"},
            },
        },
    )
    def post(self, request: Request) -> Response:
        user = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data[self.password_check_key]
        if not user.check_password(password):
            raise ValidationError(
                {self.password_check_key: "Invalid password"},
            )

        self.perform_update(serializer)

        return Response(
            {
                "detail": f"{self.update_field.capitalize()} updated successfully",
            },
            status=status.HTTP_200_OK,
        )

    def perform_update(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        setattr(
            user,
            self.update_field,
            serializer.validated_data[self.update_field],
        )
        user.save()

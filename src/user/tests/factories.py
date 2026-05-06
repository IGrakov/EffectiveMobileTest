from typing import Any, Type

import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from user import constants

User = get_user_model()

PASSWORD = "pass12345678"


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating users.
    """

    class Meta:
        model = User

    email = factory.LazyAttribute(lambda o: "%s@test.com" % f"{o.first_name}.{o.last_name}")
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    middle_name = factory.Sequence(lambda n: "middle_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)

    @classmethod
    def _create(cls, model_class: Type[User], *args: Any, **kwargs: Any) -> User:  # noqa: ANN401
        role = kwargs.pop("role", constants.Roles.DEFAULT)
        user = model_class(*args, **kwargs)
        user.set_password(kwargs.get("password", PASSWORD))

        user.save()

        user.groups.clear()

        if not user.is_superuser:
            group, _ = Group.objects.get_or_create(name=role)
        else:
            group = Group.objects.get(name=constants.Roles.ADMIN)

        user.groups.add(group)

        return user

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.db import models

from core.models import TimeStampMixin
from user.constants import Roles


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields) -> User:  # noqa ANN401
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have email")  # noqa: TRY003, EM101
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        default_group, _ = Group.objects.get_or_create(name=Roles.DEFAULT)
        user.groups.add(default_group)

        return user

    def create_superuser(self, email: str, password: str) -> User:
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        admin_group, _ = Group.objects.get_or_create(name=Roles.ADMIN)
        user.groups.clear()
        user.groups.add(admin_group)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    """Custom user model that supports email as username"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}, {self.email}"

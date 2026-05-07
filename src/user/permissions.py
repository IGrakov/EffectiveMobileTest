from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from user import constants
from user.models import User


def get_user_role_rank(user: User) -> int:
    if not user.is_active:
        return constants.Ranks.INACTIVE_USER  # disabled user has no rights

    if user.is_superuser:
        return constants.Ranks.SUPERUSER  # should be the highest rank

    if user.groups.filter(name=constants.Roles.ADMIN).exists():
        return constants.Ranks.ADMIN

    if user.groups.filter(name=constants.Roles.SUPERVISOR).exists():
        return constants.Ranks.SUPERVISOR

    if user.groups.filter(name=constants.Roles.MANAGER).exists():
        return constants.Ranks.MANAGER

    return constants.Ranks.DEFAULT_USER


class IsAdmin(IsAuthenticated):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        return get_user_role_rank(request.user) >= constants.Ranks.ADMIN


class CanManageUser(IsAuthenticated):
    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:  # noqa: ARG002
        actor = request.user

        # no one, even superuser, can perform any actions with superuser
        if obj.is_superuser:
            return False

        # superuser override and can perform actions with deleted (not active) users
        if actor.is_superuser:
            return True

        # cannot interact with inactive targets
        if not obj.is_active:
            return False

        # self access always allowed
        if obj == actor:
            return True

        actor_rank = get_user_role_rank(actor)
        target_rank = get_user_role_rank(obj)

        # only admins and superusers can manage users, only superusers can manage admins
        return actor_rank >= constants.Ranks.ADMIN and actor_rank > target_rank


class CanChangeRole(IsAuthenticated):
    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:  # noqa: ARG002
        actor = request.user

        # no one, even superuser, can perform any actions with superuser
        if obj.is_superuser:
            return False

        # superuser override and can perform actions with deleted (not active) users
        if actor.is_superuser:
            return True

        # cannot interact with inactive targets
        if not obj.is_active:
            return False

        actor_rank = get_user_role_rank(actor)
        target_rank = get_user_role_rank(obj)

        # only admins and superusers can manage users, only superusers can manage admins
        return actor_rank >= constants.Ranks.ADMIN and actor_rank > target_rank


class CanManagePermissions(IsAuthenticated):
    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:  # noqa: ARG002
        actor = request.user

        # superuser override and can perform actions with deleted (not active) users
        if actor.is_superuser:
            return True

        # cannot interact with inactive targets
        if not obj.is_active:
            return False

        actor_rank = get_user_role_rank(actor)
        target_rank = get_user_role_rank(obj)

        # only admins and superusers can manage users, only superusers can manage admins
        return actor_rank >= constants.Ranks.ADMIN and actor_rank > target_rank

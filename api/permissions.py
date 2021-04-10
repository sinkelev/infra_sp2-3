from rest_framework import permissions

from api_users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.auth and request.user.role == User.Role.ADMIN
        )


class IsStaffOrOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.auth and request.user.role == User.Role.ADMIN
            or request.auth and request.user.role == User.Role.MODERATOR
        )

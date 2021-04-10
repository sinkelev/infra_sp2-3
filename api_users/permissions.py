from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['POST', 'PATCH', 'DELETE']:
            return request.user.is_authenticated

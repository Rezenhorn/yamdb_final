from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Разрешение на действия только для admin и superuser."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение на действия только для admin,
        остальным доступ только на чтение.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (
                    request.user.is_authenticated and request.user.is_admin
                ))


class AdminModeratorOwnerOrReadOnly(
        permissions.BasePermission):
    """
    Разрешение на действия только для admin, moderator или автору комментария,
    остальным доступ только на чтение.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступно только Администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Чтение или доступно только Администратору."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorAdminModerOrReadOnly(permissions.BasePermission):
    """Чтение или доступно только Администратору/Автору/Модератору."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )

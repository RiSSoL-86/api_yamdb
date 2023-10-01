from rest_framework import permissions

from datetime import datetime


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Только чтение, если пользователь не является Администратором."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdminOrReadOnlyTitles(permissions.BasePermission):
    """Только чтение, если пользователь не является Администратором.
    Нельзя добавлять произведения которые ещё не вышли."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin and obj.year <= datetime.now)

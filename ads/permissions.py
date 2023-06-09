from rest_framework import permissions

from users.models import User


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование и удаление только авторам объявления
        # или пользователям с ролью модератора или администратора
        user = request.user
        return obj.author == user or user.role in [User.MODERATOR, User.ADMIN]

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование и удаление только авторам объекта
        return obj.owner == request.user

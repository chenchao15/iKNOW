from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('user_id') is not None

    def has_object_permission(self, request, view, competition):
        if request.method in permissions.SAFE_METHODS:
            return True
        return competition.organizer.user.id == request.session.get('user_id')


class IsNoticeOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.competition.organizer.user == request.user



from rest_framework import permissions


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            permissions.IsAuthenticated
            and obj.author == request.user
        )

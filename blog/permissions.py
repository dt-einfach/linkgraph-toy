from rest_framework import permissions


class IsEditor(permissions.BasePermission):
    """
    Custom permission to only allow Editors to interact with a resource.
    """

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, 'writer')
                and request.user.writer.is_editor
        )


class IsWriter(permissions.BasePermission):
    """
    Custom permission to only allow Writers to interact with a resource.
    """

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and hasattr(request.user, 'writer')
        )

# blog/permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit/delete it.
    Read permissions for any request, write permissions only for post author.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the author of the post or superuser
        return obj.author.user == request.user or request.user.is_superuser


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission for posts that allows:
    - Read access to everyone
    - Write access to author, staff, or superuser
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions for author, staff, or superuser
        return (obj.author.user == request.user or
                request.user.is_staff or
                request.user.is_superuser)


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Generic permission for objects with a user field
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions for owner, staff, or superuser
        return (obj.user == request.user or
                request.user.is_staff or
                request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows read access to everyone,
    but write access only to admin users
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Permission that allows access only to post authors or admin users
    """

    def has_object_permission(self, request, view, obj):
        return (obj.author.user == request.user or
                request.user.is_staff or
                request.user.is_superuser)


class CanPublishPost(permissions.BasePermission):
    """
    Permission to check if user can publish posts.
    Only staff members or superusers can publish posts directly.
    Regular users can only create drafts.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Check if trying to publish
        if request.data.get('status') == 'published':
            return request.user.is_staff or request.user.is_superuser

        return True
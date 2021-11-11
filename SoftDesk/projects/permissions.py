from rest_framework import permissions
from .models import Contributor, Project, Issue


class IsOwnerProjectOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """"
        Any authenticated user can create a new project.
        An user can update or delete a project only if he is the author of
        the project
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj.author_id == request.user.id:
                return True


class IsOwnerIssueOrCommentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """"
        Any authenticated user can create a new issue or comment.
        An user can update or delete an issue or a comment only if he is the
        author of the issue/ comment
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj.author_user.id == request.user.id:
                return True


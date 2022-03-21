from rest_framework import permissions
from api.models import Contributors, Projects, Issues
from authentication.models import User

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


class IsUser(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs["user_pk"])
        
        if user == request.user:
            return True

        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.id == request.user.id:
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False


class IsCreator(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.author == request.user:
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

class IsAuthor(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        issue = Issues.objects.get(pk=view.kwargs["issues_pk"])
        
        if request.user.is_superuser:
            return True

        if issue.project.author == request.user:
            return True

        if Contributors.objects.filter(user=request.user, project=issue.project).exists():
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False


class IsOwner(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        project = Projects.objects.get(pk=view.kwargs["projects_pk"])
        
        if project.author == request.user:
            return True

        if request.user.is_superuser:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if obj.project.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True


class IsContributor(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        project = Projects.objects.get(pk=view.kwargs["projects_pk"])
        if project.author == request.user:
            return True
        
        if Contributors.objects.filter(user=request.user, project=project).exists():
            return True

        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False

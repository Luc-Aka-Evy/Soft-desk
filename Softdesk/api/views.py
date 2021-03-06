from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from api.models import Projects, Contributors, Issues, Comments
from api.serializers import (
    ProjectsSerializer,
    ProjectsDetailSerializer,
    CommentsSerializer,
    CommentsDetailSerializer,
    ContributorsSerializer,
    ContributorsDetailSerializer,
    IssuesSerializer,
    IssuesDetailSerializer,
)
from api.permissions import IsAuthor, IsContributor, IsAdminUser, IsOwner, IsCreator

# Create your views here.


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = ProjectsDetailSerializer
    serializer_class = ProjectsSerializer
    permission_classes = [IsCreator]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        return (
            Projects.objects.filter(Q(author=self.request.user))
            | Projects.objects.filter(
                Q(contributors__in=Contributors.objects.filter(user=self.request.user))
            )[:5]
        )
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContributorsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = ContributorsDetailSerializer
    serializer_class = ContributorsSerializer
    permission_classes = [IsOwner]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs["projects_pk"])


class IssuesViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = IssuesDetailSerializer
    serializer_class = IssuesSerializer
    permission_classes = [IsContributor]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs["projects_pk"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = CommentsDetailSerializer
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthor]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        return Comments.objects.filter(issue=self.kwargs["issues_pk"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AdminProjectsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = ProjectsDetailSerializer
    serializer_class = ProjectsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Projects.objects.all()


class AdminContributorsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = ContributorsDetailSerializer
    serializer_class = ContributorsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Contributors.objects.all()


class AdminIssuesViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = IssuesDetailSerializer
    serializer_class = IssuesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Issues.objects.all()


class AdminCommentsViewset(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = CommentsDetailSerializer
    serializer_class = CommentsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Comments.objects.all()

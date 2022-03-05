from rest_framework.viewsets import ModelViewSet
from api.models import Projects, Contributors, Issues, Comments
from api.serializers import (
    ProjectsSerializer,
    CommentsSerializer,
    ContributorsSerializer,
    IssuesSerializer,
)
from api.permissions import IsAuthor, IsContributor

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
            return self.serializer_class
        return super().get_serializer_class()


class ProjectsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)


class ContributorsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs["projects_pk"])


class IssuesViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssuesSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs["projects_pk"])


class CommentsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issues_pk"])

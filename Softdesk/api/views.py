from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404
from api.models import Projects, Contributors, Issues, Comments
from api.serializers import ProjectsSerializer, CommentsSerializer, ContributorsSerializer, IssuesSerializer
from api.permissions import IsAuthor, IsContributor

# Create your views here.

class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectsSerializer 
    detail_serializer_class = ProjectsSerializer
    permission_classes = [IsAuthor]
 
    def get_queryset(self,):
        return Projects.objects.filter(author_user_id=self.request.user.id)

    @action(methods=['get'], detail=True,)
    def users(self, request, pk=None):
        """
        Returns a list of all the users working on the project
        """

        project = self.get_object()
        queryset = Contributors.objects.filter(project_id=project)
        serializer = ContributorsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True,)
    def issues(self, request, pk=None):
        """
        Returns a list of all the issues in the project
        """

        project = self.get_object()
        queryset = Issues.objects.filter(project_id=project)
        serializer = IssuesSerializer(queryset, many=True)
        return Response(serializer.data)

class ContributorsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorsSerializer
    detail_serializer_class = ContributorsSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        return Contributors.objects.all()


class CommentsViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentsSerializer
    detail_serializer_class = CommentsSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Comments.objects.all()


class IssuesViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssuesSerializer
    detail_serializer_class = IssuesSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Issues.objects.all()



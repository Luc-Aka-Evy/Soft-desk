from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer
from api.permissions import IsUser


# Create your views here.

class UserViewset(ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return User.objects.all()
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from authentication.models import User
from authentication.serializers import UserSerializer
from api.permissions import IsUser


# Create your views here.


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsUser]
    http_method_names = ["get", "put", "head", "patch", "delete"]

    def get_queryset(self):
        return User.objects.all()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

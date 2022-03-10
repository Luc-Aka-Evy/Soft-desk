from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics
from authentication.models import User
from authentication.serializers import UserSerializer
from api.permissions import IsAdminUser


# Create your views here.


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import StudentRegisterSerializer


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegisterSerializer
    permission_classes = [AllowAny]

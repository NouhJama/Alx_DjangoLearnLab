from django.shortcuts import render
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class UserRegistrationView(CreateModelMixin, APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class loginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({"message": "Login successful", "user_id": user.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


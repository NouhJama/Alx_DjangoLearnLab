from django.shortcuts import render
from .models import Post, Comment, Like, Notification
from rest_framework.viewsets import ModelViewSet
from .serializers import NotificationSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return notifications for the authenticated user only
        return self.queryset.filter(recipient=self.request.user)
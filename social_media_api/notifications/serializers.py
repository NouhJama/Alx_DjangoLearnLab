from rest_framework.serializers import ModelSerializer
from .models import Notification

# Serializer for Notification model
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']
        read_only_fields = ['id', 'timestamp']
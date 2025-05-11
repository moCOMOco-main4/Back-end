from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'Notification_id',
            'type',
            'content',
            'is_read',
            'url',
            'created_at',
        ]

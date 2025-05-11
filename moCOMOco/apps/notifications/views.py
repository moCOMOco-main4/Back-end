from rest_framework import generics, permissions , status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404




class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

class NotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            pk=notification_id,
            user=request.user
        )

        notification.is_read = True
        notification.save()
        return Response(
            {
                "Notification_id": notification.Notification_id,
                "is_read": notification.is_read
        },
        status=status.HTTP_200_OK
        )
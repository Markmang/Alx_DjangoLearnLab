from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        notif = self.get_object()
        if notif.recipient != request.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        notif.unread = False
        notif.save()
        return Response({'detail': 'Marked as read.'}, status=status.HTTP_200_OK)

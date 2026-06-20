from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class MarkReadView(APIView):
    def post(self, request, pk):
        notif = Notification.objects.filter(pk=pk, recipient=request.user).first()
        if notif:
            notif.is_read = True
            notif.save()
        return Response(status=status.HTTP_200_OK)

class MarkAllReadView(APIView):
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response(status=status.HTTP_200_OK)

class UnreadCountView(APIView):
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread_count": count})

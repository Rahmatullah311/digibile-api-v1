# tickets/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Ticket, TicketMessage, TicketAttachment
from .serializers import TicketSerializer, MessageSerializer, AttachmentSerializer


# ---- Ticket Views ----
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admins see all, users see their own tickets
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


# ---- Message Views ----
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs["ticket_id"]
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if self.request.user.is_staff or ticket.user == self.request.user:
            return TicketMessage.objects.filter(ticket=ticket)
        return TicketMessage.objects.none()

    def perform_create(self, serializer):
        attachments = self.request.FILES.getlist("attachments")
        ticket_id = self.kwargs["ticket_id"]
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if self.request.user.is_staff or ticket.user == self.request.user:
            serializer.save(ticket=ticket, sender=self.request.user)
            message = serializer.instance
            for file in attachments:
                AttachmentSerializer().create({"file": file, "message": message})
        else:
            raise PermissionDenied("You cannot post in this ticket.")


class AttachmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TicketAttachment.objects.all()

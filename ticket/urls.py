# tickets/urls.py
from django.urls import path
from .views import (
    TicketListCreateView,
    TicketDetailView,
    MessageListCreateView,
    AttachmentRetrieveUpdateDeleteView,
)

urlpatterns = [
    # Ticket Endpoints
    path("", TicketListCreateView.as_view(), name="ticket-list-create"),
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    # Message Endpoints
    path(
        "<int:ticket_id>/messages/",
        MessageListCreateView.as_view(),
        name="message-list-create",
    ),
    # Attachment Endpoints
    path(
        "attachment/<int:pk>/",
        AttachmentRetrieveUpdateDeleteView.as_view(),
        name="attachment-retrieve-update-delete",
    ),  # Optional: For retrieving/deleting attachments
]

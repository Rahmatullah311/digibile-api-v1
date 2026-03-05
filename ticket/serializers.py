# tickets/serializers.py
from rest_framework import serializers
from .models import Ticket, TicketMessage, TicketAttachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["uploaded_at"]

    def create(self, validated_data):
        print("AttachmentSerializer create called with:", validated_data)
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = TicketMessage
        fields = ["id", "ticket", "sender", "message", "created_at", "attachments"]
        read_only_fields = ["ticket", "sender", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "user",
            "subject",
            "category",
            "priority",
            "status",
            "assigned_to",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

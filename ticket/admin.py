from django.contrib import admin
from .models import Ticket, TicketMessage, TicketAttachment


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    show_change_link = True


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "category",
        "priority",
        "status",
        "user_email",
        "assigned_to_email",
        "created_at",
    )
    list_filter = ("status", "priority", "category", "created_at")
    search_fields = ("subject", "user__email", "assigned_to__email")
    date_hierarchy = "created_at"
    inlines = [TicketMessageInline]

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = "user__email"
    user_email.short_description = "User Email"

    def assigned_to_email(self, obj):
        return obj.assigned_to.email if obj.assigned_to else "-"
    assigned_to_email.admin_order_field = "assigned_to__email"
    assigned_to_email.short_description = "Assigned To"


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "sender_email", "created_at")
    search_fields = ("ticket__subject", "sender__email", "message")
    list_filter = ("created_at",)
    inlines = [TicketAttachmentInline]

    def sender_email(self, obj):
        return obj.sender.email
    sender_email.admin_order_field = "sender__email"
    sender_email.short_description = "Sender Email"


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "file", "uploaded_at")
    search_fields = ("message__ticket__subject", "message__sender__email")
    list_filter = ("uploaded_at",)

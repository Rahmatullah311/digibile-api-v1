from django.db import models
from django.conf import settings


class Ticket(models.Model):
    CATEGORY_CHOICES = [
        # Order & Delivery
        ("order_not_received", "Order Not Received"),
        ("wrong_item", "Wrong Item Delivered"),
        ("damaged_item", "Damaged Item"),
        ("late_delivery", "Late Delivery"),
        ("return_request", "Return Request"),
        ("exchange_request", "Exchange Request"),
        ("refund_request", "Refund Request"),

        # Payment & Billing
        ("payment_failed", "Payment Failed"),
        ("double_charged", "Double Charged"),
        ("payment_pending", "Payment Pending"),
        ("invoice_request", "Invoice Request"),
        ("billing_address_issue", "Billing Address Issue"),

        # Product & Listing
        ("product_not_listed", "Product Not Listed"),
        ("product_info_incorrect", "Incorrect Product Information"),
        ("out_of_stock_issue", "Out of Stock"),
        ("price_issue", "Pricing Issue"),

        # Account & Authentication
        ("account_access", "Account Access Issue"),
        ("account_verification", "Account Verification Issue"),
        ("suspicious_activity", "Suspicious Account Activity"),
        ("account_banned", "Account Banned"),

        # Coupons & Wallet
        ("coupon_invalid", "Invalid Coupon"),
        ("wallet_balance_issue", "Wallet Balance Issue"),
        ("wallet_withdrawal_issue", "Wallet Withdrawal Issue"),
        ("gift_card_issue", "Gift Card Issue"),

        # Vendor/Store
        ("vendor_registration", "Vendor Registration"),
        ("vendor_payment", "Vendor Payment Issue"),
        ("vendor_listing", "Vendor Listing Issue"),
        ("vendor_rating_review", "Vendor Rating/Review Issue"),

        # Technical & App
        ("website_bug", "Website Bug"),
        ("app_bug", "App Bug"),
        ("performance_issue", "Performance Issue"),
        ("feature_request", "Feature Request"),

        # Logistics & Shipping
        ("tracking_issue", "Tracking Issue"),
        ("shipping_partner_issue", "Shipping Partner Issue"),
        ("customs_clearance", "Customs Clearance Issue"),

        # Legal & Compliance
        ("fraud_report", "Fraudulent Activity"),
        ("counterfeit_product", "Counterfeit Product"),
        ("terms_violation", "Terms/Policy Violation"),
        ("data_privacy", "Data Privacy Request"),

        # Other
        ("general_inquiry", "General Inquiry"),
        ("feedback", "Feedback"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.subject}"

    def save(self, *args, **kwargs):
        # Auto-assign priority based on category if not manually set
        if not self.pk:  # Only on create
            self.priority = self._get_default_priority()
        super().save(*args, **kwargs)

    def _get_default_priority(self):
        urgent_categories = [
            "fraud_report", "counterfeit_product", "payment_failed",
            "double_charged", "suspicious_activity", "account_banned"
        ]
        high_categories = [
            "order_not_received", "damaged_item", "refund_request",
            "wallet_withdrawal_issue", "vendor_payment"
        ]
        medium_categories = [
            "late_delivery", "return_request", "exchange_request",
            "tracking_issue", "invoice_request"
        ]

        if self.category in urgent_categories:
            return "urgent"
        elif self.category in high_categories:
            return "high"
        elif self.category in medium_categories:
            return "medium"
        return "low"



class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_messages",
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.email} on Ticket #{self.ticket.id}"


class TicketAttachment(models.Model):
    message = models.ForeignKey(
        TicketMessage, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="ticket_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Message #{self.message.id}"

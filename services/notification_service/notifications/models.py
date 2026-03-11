from django.db import models
from common.base_models import TimeStampedModel, UUIDModel

class NotificationLog(UUIDModel, TimeStampedModel):
    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        WEBHOOK = 'webhook', 'Webhook'

    user_id = models.UUIDField(blank=True, null=True, db_index=True)
    recipient_contact = models.CharField(max_length=255) # Email hoặc SĐT
    
    channel = models.CharField(max_length=20, choices=Channel.choices)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    
    # Reference để biết mail này thuộc đơn hàng/giao dịch nào
    reference_type = models.CharField(max_length=50, blank=True) # 'order', 'payment'
    reference_id = models.UUIDField(blank=True, null=True, db_index=True)
    
    status = models.CharField(max_length=20, default='pending') # pending, sent, failed 
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.channel} to {self.recipient_contact} - {self.status}"

class EmailTemplate(UUIDModel, TimeStampedModel):
    code = models.CharField(max_length=50, unique=True) # ORDER_SUCCESS
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField() # HTML content
    variables = models.JSONField(default=list, help_text="List các biến cần có: ['order_code', 'amount']")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.base_models import TimeStampedModel, UUIDModel

class Transaction(UUIDModel, TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Đang chờ')
        PROCESSING = 'processing', _('Đang xử lý')
        SUCCESS = 'success', _('Thành công')
        FAILED = 'failed', _('Thất bại')
        REFUNDED = 'refunded', _('Hoàn tiền')
        CANCELED = 'canceled', _('Đã hủy')

    order_id = models.UUIDField(db_index=True, help_text=_("ID từ Order Service"))
    reference_id = models.CharField(max_length=100, unique=True, help_text=_("Mã giao dịch tham chiếu (Mã đơn hàng nội bộ)"))
    
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10, default='VND')
    
    provider = models.CharField(max_length=50, help_text=_("Nhà cung cấp thanh toán (e.g., vnpay, momo, stripe, banking)"))
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text=_("Phương thức thanh toán cụ thể"))
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    
    # Gateway response details
    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, help_text=_("Mã giao dịch từ Gateway trả về"))
    gateway_response_code = models.CharField(max_length=50, blank=True, null=True)
    gateway_message = models.TextField(blank=True, null=True)
    
    # Security / Webhook info
    signature = models.TextField(blank=True, null=True, help_text=_("Chữ ký số để xác thực callback"))
    
    paid_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'transactions_transaction'
        verbose_name = _('Giao dịch (Transaction)')
        verbose_name_plural = _('Các giao dịch')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id', 'status']),
            models.Index(fields=['reference_id']),
            models.Index(fields=['created_at']),
        ]
        # Đảm bảo 1 order chỉ có tối đa 1 giao dịch thành công
        # constraints = [
        #     models.UniqueConstraint(fields=['order_id'], condition=models.Q(status='success'), name='transactions_unique_successful_txn')
        # ]

    def __str__(self):
        return f"TXN {self.reference_id} - {self.get_status_display()}"


class TransactionLog(UUIDModel, TimeStampedModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='logs')
    status_from = models.CharField(max_length=20, blank=True, null=True)
    status_to = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    raw_data = models.JSONField(blank=True, null=True, help_text=_("Dữ liệu gốc (JSON JSON) từ callback của Gateway"))

    class Meta:
        db_table = 'transactions_transaction_log'
        verbose_name = _('Lịch sử giao dịch (Transaction Log)')
        verbose_name_plural = _('Lịch sử các giao dịch')
        ordering = ['-created_at']

    def __str__(self):
        return f"Log {self.transaction.reference_id}: {self.status_to}"

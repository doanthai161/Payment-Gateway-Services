from django.db import models
from common.base_models import TimeStampedModel, UUIDModel

class Order(UUIDModel, TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Chờ xác nhận'
        CONFIRMED = 'confirmed', 'Đã xác nhận'
        SHIPPING = 'shipping', 'Đang giao hàng'
        COMPLETED = 'completed', 'Hoàn thành'
        CANCELLED = 'cancelled', 'Đã hủy'

    user_id = models.UUIDField(db_index=True, help_text="ID từ User Service")
    order_code = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Financial
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Shipping Info (Snapshot)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    note = models.TextField(blank=True, null=True)
    
    # Link to Payment Service
    payment_id = models.UUIDField(blank=True, null=True, help_text="ID của transaction bên Payment")

    def __str__(self):
        return self.order_code

class OrderItem(UUIDModel, TimeStampedModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    product_id = models.UUIDField(help_text="ID từ Product Service")
    product_name = models.CharField(max_length=255) # Snapshot tên SP
    sku = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Item of Order {self.order.order_code}"
import uuid
from django.db import transaction
from .models import Order, OrderItem

class OrderService:
    @staticmethod
    @transaction.atomic # Đảm bảo toàn vẹn dữ liệu (Rollback nếu lỗi)
    def create_order(user_id, validated_data):
        items_data = validated_data['items']
        
        total_amount = 0
        for item in items_data:
            total_amount += item['quantity'] * item['unit_price']
        
        order = Order.objects.create(
            user_id=user_id,
            order_code=f"ORD{uuid.uuid4().hex[:8].upper()}",
            total_amount=total_amount,
            final_amount=total_amount, # Tạm thời chưa tính phí ship
            recipient_name=validated_data['recipient_name'],
            recipient_phone=validated_data['recipient_phone'],
            shipping_address=validated_data['shipping_address'],
            note=validated_data.get('note', ''),
            status=Order.Status.PENDING
        )
        
        order_items = [
            OrderItem(
                order=order,
                product_id=item['product_id'],
                product_name=item['product_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            ) for item in items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        
        # Gọi Payment Service để khởi tạo giao dịch
        OrderService._initiate_payment(order)
        
        return order

    @staticmethod
    def _initiate_payment(order):
        from django.conf import settings
        from utils.http_client import InternalServiceClient
        
        client = InternalServiceClient(settings.PAYMENT_SERVICE_URL)
        payload = {
            "order_id": str(order.id),
            "amount": float(order.final_amount),
            "reference_id": order.order_code,
            "provider": "banking" # Mặc định hoặc lấy từ request
        }
        
        response = client.post("/api/v1/payments/", data=payload)
        if response and response.get("id"):
            order.payment_id = response.get("id")
            order.save()
        else:
            # TODO: Xử lý lỗi khi không gọi được Payment Service
            print(f"Warning: Could not initiate payment for order {order.order_code}")
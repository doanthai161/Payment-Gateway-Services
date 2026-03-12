from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemWriteSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    product_name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)

class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemWriteSerializer(many=True)
    shipping_address = serializers.CharField()
    recipient_name = serializers.CharField(max_length=100)
    recipient_phone = serializers.CharField(max_length=20)
    note = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất một sản phẩm.")
        return value

class OrderResponseSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_code', 'status', 'total_amount', 'final_amount', 
                  'recipient_name', 'shipping_address', 'created_at']
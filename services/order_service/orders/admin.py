from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'unit_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'user_id', 'status', 'final_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_code', 'recipient_phone']
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'created_at', 'updated_at']
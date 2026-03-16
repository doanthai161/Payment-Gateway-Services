from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import CreateOrderSerializer, OrderResponseSerializer, PaymentStatusUpdateSerializer
from .services import OrderService


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(user_id=request.user.id, validated_data=serializer.validated_data)

        return Response(
            {"message": "Tạo đơn hàng thành công", "data": OrderResponseSerializer(order).data},
            status=status.HTTP_201_CREATED,
        )


class PaymentStatusUpdateView(APIView):
    """
    Internal endpoint called by Payment Service when a transaction reaches a new status.

    Secured by X-Internal-Token when INTERNAL_SERVICE_TOKEN is set.
    """

    permission_classes = [AllowAny]

    def post(self, request, order_id):
        expected = getattr(settings, "INTERNAL_SERVICE_TOKEN", "") or ""
        provided = (request.headers.get("X-Internal-Token") or "").strip()
        if expected and provided != expected:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PaymentStatusUpdateSerializer(data={**request.data, "order_id": str(order_id)})
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(id=order_id)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            payment_id = serializer.validated_data.get("payment_id")
            if payment_id:
                order.payment_id = payment_id

            payment_status = serializer.validated_data["status"]
            if payment_status == "success":
                order.status = Order.Status.CONFIRMED
            elif payment_status in {"failed", "canceled"}:
                order.status = Order.Status.CANCELLED

            order.save(update_fields=["payment_id", "status", "updated_at"])

        return Response({"status": "updated"}, status=status.HTTP_200_OK)

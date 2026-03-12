from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateOrderSerializer, OrderResponseSerializer
from .services import OrderService

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = OrderService.create_order(
            user_id=request.user.id,
            validated_data=serializer.validated_data
        )
        
        return Response({
            "message": "Tạo đơn hàng thành công",
            "data": OrderResponseSerializer(order).data
        }, status=status.HTTP_201_CREATED)
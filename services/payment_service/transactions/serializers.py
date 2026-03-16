from rest_framework import serializers

from .models import Transaction


class TransactionCreateSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    reference_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    provider = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255, required=False)


class TransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

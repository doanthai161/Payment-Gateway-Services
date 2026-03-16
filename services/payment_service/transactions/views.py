import uuid

from django.db import transaction as db_transaction
from providers.bank_factory import UnsupportedProviderError, get_provider
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction, TransactionLog
from .serializers import TransactionCreateSerializer


class CreatePaymentView(APIView):
    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            provided_reference = (serializer.validated_data.get("reference_id") or "").strip()
            reference_id = provided_reference or f"PAY-{uuid.uuid4().hex[:8].upper()}"
            if provided_reference and Transaction.objects.filter(reference_id=reference_id).exists():
                return Response({"error": "reference_id already exists"}, status=status.HTTP_409_CONFLICT)
            transaction = Transaction.objects.create(
                order_id=serializer.validated_data["order_id"],
                amount=serializer.validated_data["amount"],
                provider=serializer.validated_data["provider"],
                reference_id=reference_id,
                status=Transaction.Status.PENDING,
            )

            try:
                provider_client = get_provider(transaction.provider)
            except UnsupportedProviderError as exc:
                return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

            payment_data = provider_client.create_payment(
                amount=float(transaction.amount),
                reference_id=reference_id,
                desc=serializer.validated_data.get("description", f"Payment for order {transaction.order_id}"),
            )

            return Response(
                {"transaction_id": transaction.id, "reference_id": reference_id, "payment_data": payment_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentWebhookView(APIView):
    def post(self, request, provider):
        data = request.data
        reference_id = data.get("reference_id")

        try:
            provider_client = get_provider(provider)
        except UnsupportedProviderError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        signature = (
            request.headers.get("X-Signature")
            or request.headers.get("X-Webhook-Signature")
            or request.headers.get("X-VietQR-Signature")
        )
        mutable = dict(data)
        mutable["_raw_body"] = request.body
        mutable["_signature"] = signature
        if not provider_client.verify_callback(mutable):
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = Transaction.objects.get(reference_id=reference_id)

            new_status_raw = provider_client.webhook_to_status(mutable)
            allowed_statuses = {c for c, _ in Transaction.Status.choices}
            new_status = new_status_raw if new_status_raw in allowed_statuses else Transaction.Status.FAILED

            if transaction.status in {
                Transaction.Status.SUCCESS,
                Transaction.Status.FAILED,
                Transaction.Status.CANCELED,
                Transaction.Status.REFUNDED,
            }:
                TransactionLog.objects.create(
                    transaction=transaction,
                    status_from=transaction.status,
                    status_to=transaction.status,
                    message=f"Duplicate webhook received from {provider}",
                    raw_data=data,
                )
                return Response({"status": "duplicate"}, status=status.HTTP_200_OK)

            # Log the raw callback data
            TransactionLog.objects.create(
                transaction=transaction,
                status_from=transaction.status,
                status_to=new_status,
                message=f"Webhook received from {provider}",
                raw_data=data,
            )

            # Update transaction status
            transaction.status = new_status
            gateway_txn_id = provider_client.extract_gateway_transaction_id(mutable)
            if gateway_txn_id:
                transaction.gateway_transaction_id = gateway_txn_id
            transaction.save()

            # Notify Order Service via Celery
            if transaction.status == Transaction.Status.SUCCESS:
                from .tasks import notify_order_service

                db_transaction.on_commit(lambda: notify_order_service.delay(str(transaction.id)))

            return Response({"status": "received"}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

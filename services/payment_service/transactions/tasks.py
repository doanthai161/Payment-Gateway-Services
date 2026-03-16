import logging

import requests
from celery import shared_task
from django.conf import settings

from .models import Transaction

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def notify_order_service(self, transaction_id):
    """Notify the Order Service about a payment status change."""
    try:
        transaction = Transaction.objects.get(id=transaction_id)

        order_callback_url = f"{settings.ORDER_SERVICE_URL}/api/v1/orders/{transaction.order_id}/payment-status/"

        payload = {
            "order_id": str(transaction.order_id),
            "status": transaction.status,
            "reference_id": transaction.reference_id,
            "gateway_transaction_id": transaction.gateway_transaction_id,
            "payment_id": str(transaction.id),
        }

        logger.info(f"Notifying Order Service for transaction {transaction.reference_id}")

        headers = {}
        token = getattr(settings, "INTERNAL_SERVICE_TOKEN", "") or ""
        if token:
            headers["X-Internal-Token"] = token

        response = requests.post(order_callback_url, json=payload, headers=headers, timeout=5)
        if response.status_code >= 400:
            raise requests.HTTPError(
                f"Order Service responded {response.status_code}: {response.text}",
                response=response,
            )

        logger.info(f"Successfully notified Order Service for {transaction.reference_id}")
        return True

    except Transaction.DoesNotExist:
        logger.error(f"Transaction {transaction_id} not found for notification")
        return False
    except Exception as exc:
        logger.warning(f"Error notifying Order Service: {exc}. Retrying...")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def check_pending_transactions():
    """Periodic task to poll providers for pending transactions."""
    pending_txns = Transaction.objects.filter(status="pending")
    for txn in pending_txns:
        # Here you would call the query_transaction method of the provider
        logger.info(f"Checking status for pending transaction {txn.reference_id}")
        pass

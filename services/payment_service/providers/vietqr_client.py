import hashlib
import hmac
import logging
from typing import Any, Dict

from django.conf import settings

from .base_provider import BasePaymentProvider

logger = logging.getLogger(__name__)


class VietQRProvider(BasePaymentProvider):
    def create_payment(self, amount: float, reference_id: str, desc: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"Creating VietQR payment for {reference_id} with amount {amount}")

        # Mocking VietQR payload generation.
        # In real world, this might call an API to get a QR content or just generate a string.
        qr_content = (
            "00020101021238580010A0000007270128000697040301140722101234567852045814"
            f"53037045405{int(amount)}5802VN62150811{desc[:10]}6304ABCD"
        )

        return {
            "status": "success",
            "qr_content": qr_content,
            "qr_url": f"https://api.vietqr.io/image/970403/123456789/{int(amount)}/{reference_id}.jpg",
            "reference_id": reference_id,
        }

    def verify_callback(self, data: Dict[str, Any]) -> bool:
        secret = getattr(settings, "VIETQR_WEBHOOK_SECRET", "") or ""
        if not secret:
            logger.warning("VIETQR_WEBHOOK_SECRET is empty; skipping signature verification")
            return True

        raw_body: bytes = data.get("_raw_body", b"")
        signature: str = (data.get("_signature") or "").strip()
        if not raw_body or not signature:
            return False

        expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def query_transaction(self, reference_id: str) -> Dict[str, Any]:
        return {"status": "COMPLETED", "amount": 100000, "reference_id": reference_id}

    def webhook_to_status(self, data: Dict[str, Any]) -> str:
        raw = (data.get("status") or data.get("payment_status") or "").strip().lower()
        if raw in {"success", "paid", "completed", "ok"}:
            return "success"
        if raw in {"pending", "processing"}:
            return "processing"
        if raw in {"failed", "error", "canceled", "cancelled"}:
            return "failed"
        if data.get("paid") is True:
            return "success"
        return "failed"

    def extract_gateway_transaction_id(self, data: Dict[str, Any]) -> str | None:
        return data.get("vietqr_transaction_id") or data.get("gateway_transaction_id") or data.get("transaction_id")

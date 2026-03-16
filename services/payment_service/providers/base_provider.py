from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePaymentProvider(ABC):
    """Base class for all payment gateway providers (VNPAY, Momo, VietQR, etc.)."""

    @abstractmethod
    def create_payment(self, amount: float, reference_id: str, desc: str, **kwargs) -> Dict[str, Any]:
        """Send request to gateway to create a payment session/URL."""
        raise NotImplementedError

    @abstractmethod
    def verify_callback(self, data: Dict[str, Any]) -> bool:
        """Verify the signature and data received from gateway callback."""
        raise NotImplementedError

    @abstractmethod
    def query_transaction(self, reference_id: str) -> Dict[str, Any]:
        """Query current status of a transaction from gateway."""
        raise NotImplementedError

    def webhook_to_status(self, data: Dict[str, Any]) -> str:
        """Map provider webhook payload to an internal Transaction.Status value."""
        return "success"

    def extract_gateway_transaction_id(self, data: Dict[str, Any]) -> str | None:
        """Extract provider transaction id from webhook payload, if present."""
        return data.get("gateway_transaction_id") or data.get("transaction_id")

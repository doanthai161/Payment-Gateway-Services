from __future__ import annotations

from dataclasses import dataclass

from .base_provider import BasePaymentProvider
from .vietqr_client import VietQRProvider


@dataclass(frozen=True)
class UnsupportedProviderError(ValueError):
    provider: str

    def __str__(self) -> str:
        return f"Unsupported provider: {self.provider}"


_PROVIDER_MAP: dict[str, type[BasePaymentProvider]] = {
    "vietqr": VietQRProvider,
    "banking": VietQRProvider,  # default/mock until a real banking provider is implemented
}


def get_provider(provider_code: str) -> BasePaymentProvider:
    provider_code = (provider_code or "").strip().lower()
    provider_cls = _PROVIDER_MAP.get(provider_code)
    if not provider_cls:
        raise UnsupportedProviderError(provider=provider_code or "<empty>")
    return provider_cls()

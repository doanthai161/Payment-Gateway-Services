from django.urls import path

from .views import CreateOrderView, PaymentStatusUpdateView

urlpatterns = [
    path("", CreateOrderView.as_view(), name="create-order"),
    path("<uuid:order_id>/payment-status/", PaymentStatusUpdateView.as_view(), name="payment-status"),
]

from django.urls import path

from .views import CreatePaymentView, PaymentWebhookView

urlpatterns = [
    path("payments/", CreatePaymentView.as_view(), name="create-payment"),
    path("payments/webhook/<str:provider>/", PaymentWebhookView.as_view(), name="payment-webhook"),
]

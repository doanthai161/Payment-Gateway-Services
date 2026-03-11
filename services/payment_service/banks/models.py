from django.db import models
from common.base_models import TimeStampedModel, UUIDModel

class PaymentGateway(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    # Lưu config dạng JSON, cần mã hóa ở Application Layer trước khi lưu
    config = models.JSONField(default=dict) 

    def __str__(self):
        return self.name
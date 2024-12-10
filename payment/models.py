from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_phone = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)

    # Tự chỉ định chính xác dạng số nhiều không cho django tự thêm dạng số nhiều s/es
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

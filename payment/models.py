from django.db import models
from django.contrib.auth.models import User
from store.models import Product

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
    

# Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.DecimalField(max_digits=20, decimal_places=0)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return f'Order - {str(self.id)}'
    
# Order Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=0)

    def __str__(self):
        return f'Order Item - {str(self.id)}'




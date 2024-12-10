from django.contrib import admin
from .models import OrderItem, ShippingAddress, Order

# Register model
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

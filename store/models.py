from django.db import models
from datetime import datetime

#Categories of products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

#Customer
class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname

#All of our product
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    #sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=20)
    def __str__(self):
        return self.name

#Customer order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quanlity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True, )
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'


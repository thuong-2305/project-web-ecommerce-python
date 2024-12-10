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
    description = models.CharField(max_length=10000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    #configure
    config = models.CharField(max_length=10000, default='', blank=True, null=True)
    #sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=20)
    def __str__(self):
        return self.name

    def get_discounted_price(self):
        active_sales = SaleEvent.objects.filter(
            category=self.category,
            start_date__lte=datetime.now(),
            end_date__gte=datetime.now()
        ).order_by('-discount_percentage')  # Nếu có nhiều giảm giá lấy cái nào giảm nhiều nhất

        if active_sales.exists():
            sale = active_sales.first()
            discounted_price = self.price * (1 - sale.discount_percentage / 100)

            self.sale_price = discounted_price
            self.is_sale = True
            self.save()

            return discounted_price

        # Nếu không có đợt giảm giá, trả về giá gốc và sale_price vẫn bằng 0 trong csdl
        return self.price

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

#SaleEvent
class SaleEvent(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return f"Sale for {self.category.name} ({self.discount_percentage}%)"

    def is_active(self):
        """Kiểm tra đợt giảm giá còn hiệu lực không."""
        now = datetime.now()
        return self.start_date <= now <= self.end_date




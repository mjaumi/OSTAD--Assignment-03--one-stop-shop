from django.db import models
from products.models import Product, TimeStampedModel
from accounts.models import CustomUser

class Payment(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

# Order model to store order details
class Order(TimeStampedModel):
    STATUS = [('New', 'New'),
              ('Accepted', 'Accepted'),
              ('Completed', 'Completed'),
              ('Cancelled', 'Cancelled')
            ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20, unique=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='New')

# OrderProduct model to store product details in an order
class OrderProduct(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

from django.db import models
from accounts.models import CustomUser
from products.models import Product, TimeStampedModel

# Cart model
class Cart(TimeStampedModel):
    session_key = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.session_key
    
# CartItem model
class CartItem(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.discount_price * self.quantity
    
    def __str__(self):
        return f'CART ITEM: {self.product.name}'
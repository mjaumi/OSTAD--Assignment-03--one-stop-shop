from django.db import models
from products.models import Product, TimeStampedModel
from accounts.models import CustomUser

# Review model
class Review(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
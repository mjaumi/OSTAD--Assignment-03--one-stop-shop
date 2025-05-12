from django.db import models

# Abstract base class for models that need timestamps
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Product model
class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    processor = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    camera = models.CharField(max_length=255)


    image = models.ImageField(upload_to='products/')

    @property
    def discount_price(self):
        if self.discount_percentage > 0:
            return self.price - (self.price * self.discount_percentage / 100)
        return self.price

    class Meta:
        ordering = ("created_at",)
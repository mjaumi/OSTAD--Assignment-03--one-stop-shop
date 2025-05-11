from django.contrib.auth.models import AbstractUser
from django.db import models

from  .managers import CustomUserManager

# Creating custom user model here
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # set the email field as the unique identifier for the user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    objects = CustomUserManager()



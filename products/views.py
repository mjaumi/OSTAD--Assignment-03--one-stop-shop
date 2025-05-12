from django.shortcuts import render
from .models import Product

# Home page view
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
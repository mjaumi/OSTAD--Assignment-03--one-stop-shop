from django.shortcuts import render
from .models import Product

# Home page view
def home(request):
    products = Product.objects.all()
    featured_products = Product.objects.filter(is_featured=True)

    return render(request, 'home.html', {
        'products': products,
        'featured_products': featured_products
    })

# Product details view
def product_details(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_details.html', {'product': product})
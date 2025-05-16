from django.shortcuts import render, redirect
from .models import Product, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    reviews = product.reviews.all()

    return render(request, 'product_details.html', {'product': product, 'reviews': reviews})

# Create your views here.
@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')

        product = Product.objects.get(pk=product_id)
        user = request.user

        # Assuming you have a Review model
        review = Review.objects.create(product=product, user=user, review_text=review_text)
        review.save()

        messages.success(request, 'Review added successfully!')

    # Redirect back to the same page after adding a review
    url = request.META.get('HTTP_REFERER')
    return redirect(url)  
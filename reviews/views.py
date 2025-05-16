from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product

from .models import Review

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
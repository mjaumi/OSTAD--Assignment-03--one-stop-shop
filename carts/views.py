from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .utils import get_session_key

from .models import Cart, CartItem
from products.models import Product

# Add to cart view
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # finding existing cart if not create new one
    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            session_key=request.session.session_key, 
            user=request.user if request.user.is_authenticated else None
        )

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart)
        

    messages.success(request, 'Item added to cart successfully!')

    # Redirect back to the same page after adding to cart
    url = request.META.get('HTTP_REFERER')
    return redirect(url)

# Remove from cart view
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart = get_object_or_404(Cart, session_key=request.session.session_key)

    cart_item = get_object_or_404(CartItem, product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')

    # Redirect back to the same page after adding to cart
    url = request.META.get('HTTP_REFERER')
    return redirect(url)

# Cart details view
def cart_details(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = get_session_key(request)
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    total_price = sum(item.sub_total() for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'quantity': quantity
    }

    return render(request, 'cart_details.html', context)
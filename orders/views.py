import datetime
import random
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

from sslcommerz_python_api import SSLCSession

from carts.models import Cart, CartItem
from products.models import Product

from .models import Order, OrderProduct, Payment

# Place order view
@csrf_exempt
@login_required
def place_order(request):
    current_user = request.user

    cart = get_object_or_404(Cart, user=current_user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    cart_item_count = cart_items.count()

    if cart_item_count <= 0:
        messages.error(request, 'Your cart is empty!')
        return redirect('home')
    
    total = sum(item.product.discount_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        try:
            current_date = datetime.date.today()

            order_number = current_date.strftime('%Y%m%d') + str(random.randint(1000, 9999))

            order = Order.objects.create(
                user=current_user,
                order_number=order_number,
                mobile=current_user.phone_number,
                email=current_user.email,
                address=current_user.address,
                country=current_user.country,
                postal_code=current_user.postal_code,
                city=current_user.city,
                order_total = total,
            )

            for item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    user=current_user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.discount_price,
                )

                # Updating product stock here
                product = Product.objects.get(id=item.product.id)

                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    messages.error(request, f'Insufficient stock for {item.product.name}.')
                    return redirect('cart_details')
                
                # Clear the cart after order is placed
                item.delete()
            
            return redirect('payment')


        except Exception as e:
            messages.error(request, 'An error occurred while processing your order.')
            return redirect('home')

    context = {
        'user': current_user,
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'checkout.html', context)

@login_required
def payment(request):
    order_payment = SSLCSession(
        sslc_is_sandbox=True,
        sslc_store_id="testbox",
        sslc_store_pass="qwerty"
    )

    status_url = request.build_absolute_uri('status/')

    order_payment.set_urls(
        success_url=status_url,
        fail_url=status_url,
        cancel_url=status_url,
        ipn_url=status_url,
    )

    user = request.user
    unpaid_order = Order.objects.filter(user=user, status='Pending').last()

    order_payment.set_product_integration(
        total_amount=Decimal(unpaid_order.order_total),
        currency='USD',
        product_category='gadgets',
        product_name='Gadgets',
        num_of_item=2,
        shipping_method='YES',
        product_profile='None',
    )

    order_payment.set_customer_info(
        name=user.first_name + ' ' + user.last_name,
        email=user.email,
        address1=user.address,
        address2='',
        city=user.city, 
        postcode=user.postal_code,
        country=user.country,
        phone=user.phone_number,
    )

    order_payment.set_shipping_info(
        shipping_to=user.first_name + ' ' + user.last_name,
        address=user.address,
        city=user.city,
        postcode=user.postal_code,
        country=user.country
    )

    
    response = order_payment.init_payment()

    print('SSL COMMERZ RESPONSE: ', response, settings.SSLCOMMERZ_IS_SANDBOX, settings.SSLCOMMERZ_STORE_ID, settings.SSLCOMMERZ_STORE_PASS)

    if response['status'] != 'SUCCESS':
        messages.error(request, response['failedreason'])
        return redirect('home')
    
    return redirect(response['GatewayPageURL'])

# Payment status view
@csrf_exempt
def payment_status(request):
    if request.method == 'POST':
        payment_data = request.POST

        if payment_data['status'] == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            payment_method = payment_data.get("card_type", "Unknown")

            return HttpResponseRedirect(
                reverse('sslc_complete', 
                        kwargs={'tran_id': tran_id, 'payment_method': payment_method})
            )
        else:
            messages.error(request, 'Payment failed! Please try again.')
            return redirect('home')
        
    
    return render(request, 'status.html')


def sslc_complete(request, tran_id, payment_method):
    try:
        unpaid_order = Order.objects.filter(user=request.user, status='Pending').last()

        payment = Payment.objects.create(
            user=request.user,
            payment_id=tran_id,
            payment_method=payment_method,
            amount_paid=unpaid_order.order_total,
            status='Completed',
        )

        unpaid_order.payment = payment
        unpaid_order.status = 'Completed'
        unpaid_order.save()

        # delete the cart after successful payment
        Cart.objects.filter(user=request.user).delete()

        context = {
            'order': unpaid_order,
            'transaction_id': tran_id,
        }

        return render(request, 'status.html', context)

    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('home')
    except Exception as e:
        messages.error(request, 'An error occurred while processing your payment.')
        return redirect('home')


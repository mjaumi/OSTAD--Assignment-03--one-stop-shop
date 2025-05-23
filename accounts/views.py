from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm, UpdateUserDashboardForm
from .utils import send_verification_email
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm

from orders.models import Order

from .models import CustomUser

# user registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)

        print(form.errors)
        
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.success(request, 'Registration successful! Please check your email for verification.')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
        
    return render(request, 'register.html')

# user email verification view
def verify_email(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired verification link!')
        return redirect('register')

# user login view
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, 'Invalid email or password!')
        elif not user.is_verified:
            messages.error(request, 'Email not verified! Please check your email for verification.')
        else:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')

    return render(request, 'login.html')

# user dashboard view
@login_required
def user_dashboard(request):
    user = request.user
    user_orders = Order.objects.filter(user=user).order_by('-created_at')
    user_reviews = user.reviews.all()

    return render(request, 'dashboard.html', {'user': user, 'orders': user_orders, 'reviews': user_reviews})

# update user dashboard view
@login_required
def update_user_dashboard(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateUserDashboardForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UpdateUserDashboardForm(instance=user)

    return render(request, 'update_dashboard.html', {'user': user})

# change password view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')
        else:
            return render(request, 'change_password.html', {'form': form})
        
    return render(request, 'change_password.html')

# user logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')
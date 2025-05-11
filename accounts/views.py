from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from .utils import send_verification_email
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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


def login(request):
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from .utils import send_verification_email
from django.contrib import messages

# Create your views here.
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

def login(request):
    return render(request, 'login.html')

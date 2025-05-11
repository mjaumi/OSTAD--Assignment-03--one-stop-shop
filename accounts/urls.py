from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('verify/<uid64>/<token>/', views.verify_email, name='verify_email'),
]
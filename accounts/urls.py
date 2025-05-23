from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/<uid64>/<token>/', views.verify_email, name='verify_email'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('dashboard/update/', views.update_user_dashboard, name='update_dashboard'),
    path('dashboard/change/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
]
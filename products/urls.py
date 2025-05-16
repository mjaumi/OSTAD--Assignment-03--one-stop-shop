from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    path('review/remove/<int:review_id>/', views.remove_review, name='remove_review')
]
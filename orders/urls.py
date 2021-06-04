from django.urls import path
from .views import addToCart

urlpatterns = [
    path('buy<int:productId>/', addToCart),
]
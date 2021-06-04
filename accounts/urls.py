from django.urls import path
from .views import register, login, logout, userProfilePage

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('<int:uid>/', userProfilePage)
]
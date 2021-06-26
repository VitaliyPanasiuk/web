from django.urls import path
from .views import register, login, logout, userProfilePage, userOrders, userCart, userFavourites, editProfilePage, editPasswordPage

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('<int:uid>/', userProfilePage),
    path('<int:uid>/orders', userOrders),
    path('<int:uid>/cart', userCart),
    path('<int:uid>/favourites', userFavourites),
    path('<int:uid>/edit', editProfilePage),
    path('<int:uid>/change-password', editPasswordPage)
]
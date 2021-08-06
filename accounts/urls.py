from django.urls import path
from .views import register, login, logout, userProfilePage, userOrders, userCart, userFavourites, editProfilePage, editPasswordPage, makeOrder, edit_order_page, orderInfo, success_order

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('<int:uid>/', userProfilePage),
    path('<int:uid>/orders', userOrders),
    path('<int:uid>/cart', userCart),
    path('<int:uid>/favourites', userFavourites),
    path('<int:uid>/edit', editProfilePage),
    path('<int:uid>/change-password', editPasswordPage),
    path('<int:uid>/make-order', makeOrder),
    path('<int:uid>/order/<int:oid>', orderInfo),
    path('<int:uid>/success-order', success_order),
    path('<int:uid>/edit-order/<int:oid>', edit_order_page),
]
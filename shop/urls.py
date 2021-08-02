from django.urls import path
from .views import homePage, productsPage, achievementsPage, aboutUsPage, aboutProductPage, searchPage

urlpatterns = [
    path('', homePage),
    path('products/', productsPage),
    path('achievements/', achievementsPage),
    path('about/', aboutUsPage),
    path('product/<int:id>/', aboutProductPage),
    path('products/search/', searchPage),
]

handler404 = 'shop.views.error404'
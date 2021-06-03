from django.urls import path
from .views import homePage, productsPage, achievementsPage, aboutUsPage, loginPage, aboutProductPage

urlpatterns = [
    path('', homePage),
    path('products/', productsPage),
    path('achievements', achievementsPage),
    path('about', aboutUsPage),
    path('products/<int:id>/', aboutProductPage),
]

handler404 = 'shop.views.error404'
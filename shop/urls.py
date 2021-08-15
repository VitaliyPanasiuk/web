from django.urls import path
from .views import homePage, productsPage, achievementsPage, aboutUsPage, aboutProductPage, searchPage, goWithLanguage

urlpatterns = [
    #RUSSIAN
    path('<str:lang>/', homePage),
    path('<str:lang>/products/', productsPage),
    path('<str:lang>/achievements/', achievementsPage),
    path('<str:lang>/about/', aboutUsPage),
    path('<str:lang>/product/<int:id>/', aboutProductPage),
    path('<str:lang>/products/search/', searchPage),
    path('', goWithLanguage)
]

handler404 = 'shop.views.error404'
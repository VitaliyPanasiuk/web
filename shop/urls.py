from django.urls import path
from .views import (
    homePage,
    productsPage,
    achievementsPage,
    aboutUsPage,
    aboutProductPage,
    searchPage,
    collaborationPage,
    guaranteesPage,
    goWithLanguage,
)


urlpatterns = [
    path("<str:lang>/", homePage),
    path("<str:lang>/products/", productsPage),
    path("<str:lang>/achievements/", achievementsPage),
    path("<str:lang>/about/", aboutUsPage),
    path("<str:lang>/product/<int:id>/", aboutProductPage),
    path("<str:lang>/collaboration/", collaborationPage),
    path("<str:lang>/guarantees/", guaranteesPage),
    path("<str:lang>/products/search/", searchPage),
    path("<str:lang>/products/fromStartPage/", searchPage),
    path("", goWithLanguage),
]

handler404 = "shop.views.error404"

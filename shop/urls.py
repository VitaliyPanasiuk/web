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
'''categoryPage,
    categorySearchPage,'''

urlpatterns = [
    path("<str:lang>/", homePage),
    path("<str:lang>/products/", productsPage),
    path("<str:lang>/achievements/", achievementsPage),
    path("<str:lang>/about/", aboutUsPage),
    path("<str:lang>/product/<int:id>/", aboutProductPage),
    path("<str:lang>/collaboration/", collaborationPage),
    path("<str:lang>/guarantees/", guaranteesPage),
    path("<str:lang>/products/search/", searchPage),
    #path("<str:lang>/products/category/<int:id>/", categoryPage),
    #path("<str:lang>/products/category/<int:id>/search/", categorySearchPage),
    path("", goWithLanguage),
]

handler404 = "shop.views.error404"

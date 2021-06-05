from django import forms
from django.db import models
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Продукт
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse

продукты = Продукт.objects.all()
x = 0
y = 4

def homePage(request):
    return render(request, 'shop/index.html')


def productsPage(request):
    context = {
        'продукты': продукты[len(продукты)-20:len(продукты):],
            }
    template = 'products/index.html'
    return render(request, template, context)

def error404(request, exception):
    return render(request, '404.html')

def achievementsPage(request):
    return render(request, 'achievements/index.html')

def aboutUsPage(request):
    return render(request, 'about/index.html')

def loginPage(request):
    return render(request, 'login/index.html')

def aboutProductPage(request, id):
    context = {
        'продукт': продукты[id-1],
    }
    template = 'productInfo/more.html'
    return render(request, template, context)

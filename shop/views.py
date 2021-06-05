from django.shortcuts import render, redirect
from .models import Продукт
from django.template.context_processors import csrf
import json
from django.http import HttpResponse
from .models import ShopCart

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
    context.update(csrf(request))
    if request.POST:
        itemToAdd = request.POST.get('add', '')
        if itemToAdd:
            ToSave = ShopCart(user_id=request.user.id, item=itemToAdd)
            ToSave.save()
            return redirect('/products')
        else:
            return HttpResponse('bad')
    
    else:
        return render(request, template, context)

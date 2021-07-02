from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.http import HttpResponse
from .models import Продукт
from django.db import models

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

    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_cart'

    carts = ShopCarty.objects.all()

    class ShopFavourite(models.Model):
        favourite_id = models.AutoField(primary_key=True)
        user_id = models.CharField(max_length=45)
        favourite_item = models.CharField(max_length=45, blank=True, null=True)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=45, blank=True, null=True)
        currency = models.CharField(max_length=45, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_favourite'
        
    favourites = ShopFavourite.objects.all()

    context = {
        'продукт': продукты[id-1],
        'user_id': request.user.id,
    }
    template = 'productInfo/more.html'
    context.update(csrf(request))
    if request.POST:
        cart_add = request.POST.get('add_to_cart', '')
        favourite_add = request.POST.get('add_to_favourite', '')
        if cart_add:
            item_id = request.POST.get('add_id', '')
            item_name = request.POST.get('add_name', '')
            item_price = request.POST.get('add_price', '')
            item_currency = request.POST.get('add_currency', '')
            howMuchToAdd = request.POST.get('how_much_to_add', '')
            ToSave = ShopCarty(user_id=request.user.id, item=item_id, name=item_name, price=item_price, currency=item_currency)
            ToSave.save()
            cart_item = ShopCarty.objects.all()
            for i in cart_item:
                if i.amount:
                    ToSave.amount = i.amount + int(howMuchToAdd) - 1
                else:
                    ToSave.amount = i.amount + int(howMuchToAdd)
            for i in carts:
                if i.amount != ToSave.amount and i.item == ToSave.item:
                    ShopCarty.objects.filter(item = ToSave.item).delete()
                elif i.amount == ToSave.amount and i.item == ToSave.item: 
                    ShopCarty.objects.filter(item = ToSave.item).delete()           
            ToSave.save()
            return redirect('/accounts/'+ str(request.user.id) +'/cart')
        elif favourite_add:
            favourite_item_id = request.POST.get('favourite_add_id', '')
            favourite_item_name = request.POST.get('favourite_add_name', '')
            favourite_item_price = request.POST.get('favourite_add_price', '')
            favourite_item_currency = request.POST.get('favourite_add_currency', '')
            favouriteToSave = ShopFavourite(user_id=request.user.id, favourite_item=favourite_item_id, name=favourite_item_name, price=favourite_item_price, currency=favourite_item_currency)
            favouriteToSave.save()
            favourite_item = ShopFavourite.objects.all()
            for i in favourite_item:
                if i.favourite_item == favourite_item_id:
                    ShopFavourite.objects.filter(favourite_item = favourite_item_id).delete()    
            favouriteToSave.save()             
            return redirect('/accounts/'+ str(request.user.id) +'/favourites')
        else:
            return HttpResponse('bad')
    
    else:
        return render(request, template, context)

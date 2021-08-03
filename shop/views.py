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
    page = request.GET.get('page')
    if page == None:
        return redirect('/products/?page=1')
    if int(page) <= 0:
        return redirect('/products/?page=1')
    counter = 20
    if request.POST:
        nextPage = request.POST.get('nextPage', '')
        previousPage = request.POST.get('previousPage', '')
        go = request.POST.get('go', '')
        gototext = request.POST.get('goto', '')
        search = request.POST.get('search', '')
        searchTextRaw = request.POST.get('searchtext', '')
        searchText = searchTextRaw.replace(" ", "-")
        if nextPage:
            intPage = int(page) + 1
            return redirect('/products/?page=' + str(intPage))
        elif previousPage:
            intPage = int(page) - 1
            return redirect('/products/?page=' + str(intPage))
        elif go:
            try:
                intPage = int(gototext)
                return redirect('/products/?page=' + str(intPage))
            except ValueError:
                return redirect('/products/?page=' + page)
        elif search:
            return redirect('/products/search/?q=' + searchText)
            '''template = 'products/search/index.html'
            a = []
            searchStr = searchText.split(" ")
            for i in продукты:
                if len(set(searchStr).intersection(i.название_позиции.split(' '))) >= 1:
                    a.append(i)
            context = {
                'продукты': a[0:len(a):],
                'page': int(page),
                }
            return render(request, template, context)'''
    if  int(page) == 1:
        context = {
            'продукты': продукты[0:counter:],
            'page': int(page),
                }
    else:
        '''for i in продукты:
            if i.наличие == '+':
                продукты.remove(i)
                продукты.append(i)
            elif i.наличие == '-':
                продукты.remove(i)
                продукты.append(i)'''
        context = {
            'продукты': продукты[counter*(int(page)-1):counter*int(page):],
            'page': int(page),
                }
    template = 'products/index.html'
    return render(request, template, context)

def searchPage(request):
    q = request.GET.get('q').replace("-", " ").lower()
    if request.POST:
        search = request.POST.get('search', '')
        searchTextRaw = request.POST.get('searchtext', '')
        searchText = searchTextRaw.replace(" ", "-")
        if search:
            return redirect('/products/search/?q=' + searchText)
    else:
        template = 'products/search/index.html'
        a = []
        #searchStr = searchText.split(" ")
        for i in продукты:
            if len((set(q.split(" ")).intersection(i.название_позиции.lower().split(' ')))) >= len(q.split(" ")):
                a.append(i)
        context = {
            'продукты': a[0:len(a):],
            #'page': int(page),
            }
        return render(request, template, context)
    #return HttpResponse(q.replace("-", " "))

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
            ToSave = ShopCarty(user_id=request.user.id, item=item_id, name=item_name, price=max(float(i) for i in item_price.replace(',','.').split()), currency=item_currency)
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
            return redirect('/products/')
        elif favourite_add:
            favourite_item_id = request.POST.get('favourite_add_id', '')
            favourite_item_name = request.POST.get('favourite_add_name', '')
            favourite_item_price = request.POST.get('favourite_add_price', '')
            favourite_item_currency = request.POST.get('favourite_add_currency', '')
            if favourite_item_price == 'None':
                favourite_item_price = 0
                favouriteToSave = ShopFavourite(user_id=request.user.id, favourite_item=favourite_item_id, name=favourite_item_name, price=favourite_item_price, currency=favourite_item_currency)
            else:
                favouriteToSave = ShopFavourite(user_id=request.user.id, favourite_item=favourite_item_id, name=favourite_item_name, price=max(float(i) for i in favourite_item_price.replace(',','.').split()), currency=favourite_item_currency)
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

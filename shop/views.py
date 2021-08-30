from django.http.response import Http404
from accounts.models import AuthUser
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.http import HttpResponse
from .models import Продукт, ShopCalls
from django.db import models
import requests
from requests.exceptions import MissingSchema
from datetime import datetime

продукты = Продукт.objects.all()

x = 0
y = 4

def homePage(request, lang):
    language = request.POST.get('language', '')
    if request.POST:
        if language:
            return redirect('/' + str(language))
        else:
            HttpResponse('404')
    else:
        context = { 
            'lang': lang,
        }
        return render(request, str(lang) + '/shop/index.html', context)


def productsPage(request, lang):
    '''for i in продукты:
        try:
            image = i.ссылка_изображения
            response = requests.get(image)
            product = Продукт.objects.get(id=i.id)
            file = open(str(i.id)+'.png', "wb")
            file.write(response.content)
            product.image = file
            product.save()
            import os
            file.close() 
            if os.path.exists(str(i.id)+".png"):
                os.remove(str(i.id)+".png")
        except MissingSchema:
            pass'''
    '''for i in продукты:
        import os
        from pathlib import Path
        try:
            images_path = 'shop/media/products/'
            product = Продукт.objects.get(id=i.id) 
            #images = open(images_path+str(i.id)+'.png', 'wb')
            #print(images.name) 
            tosave = 'products/'+str(i.id) +'.png'
            product.image = tosave
            product.save() 
            #images.close() 
        except MissingSchema:
            pass'''      

    if request.POST:
        search = request.POST.get('search', '')
        searchTextRaw = request.POST.get('searchtext', '')
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get('applyfilters', '')
        nofilters = request.POST.get('nofilters', '')
        language = request.POST.get('language', '')
        if search:
            return redirect('/' + str(lang) + '/products/search/?q=' + searchText)
        elif applyfilters:
            pricefilter = request.POST.get('pricefilter', '')
            availablefilter = request.POST.get('availablefilter', '')
            if pricefilter == 'Цена есть' and availablefilter == 'Есть':
                filteredProducts = Продукт.objects.exclude(цена=None).exclude(наличие='-')#| Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                context = {
                    'продукты': filteredProducts,
                    'withprice': 'yes',
                    'available': 'yes',
                    'lang': lang,
                        }
                template = str(lang) + '/products/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цена есть' and availablefilter == 'Нету':
                filteredProducts = Продукт.objects.exclude(цена=None).filter(наличие='-')
                context = {
                    'продукты': filteredProducts,
                    'withprice': 'yes',
                    'available': 'no',
                    'lang': lang,
                        }
                template = str(lang) + '/products/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цены нет' and availablefilter == 'Нету':
                filteredProducts = Продукт.objects.filter(цена=None).filter(наличие='-')
                context = {
                    'продукты': filteredProducts,
                    'withprice': 'no',
                    'available': 'no',
                    'lang': lang,
                        }
                template = str(lang) + '/products/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цены нет' and availablefilter == 'Есть':
                filteredProducts = Продукт.objects.exclude(наличие='-').filter(цена=None)
                context = {
                    'продукты': filteredProducts,
                    'withprice': 'no',
                    'available': 'yes',
                    'lang': lang,
                        }
                template = str(lang) + '/products/index.html'
                return render(request, template, context)
        elif nofilters:
            context = {
                'продукты': продукты,
                'withprice': 'spec',
                'available': 'spec',
                'lang': lang,
                    }
            template = str(lang) + '/products/index.html'
            return render(request, template, context)
        elif language:
            return redirect('/' + str(language))

    filteredProducts = Продукт.objects.exclude(наличие='-').exclude(цена=None)#| Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
    context = {
        'продукты': filteredProducts,
        'available': 'spec',
        'lang': lang,
            }
    template = str(lang) + '/products/index.html'
    return render(request, template, context)

def searchPage(request, lang):
    q = request.GET.get('q').replace("-", " ").lower()
    a = Продукт.objects.filter(название_позиции__icontains = q)
    if request.POST:
        page = 1
        counter = 20
        search = request.POST.get('search', '')
        searchTextRaw = request.POST.get('searchtext', '')
        searchText = searchTextRaw.replace(" ", "-")
        applyfilters = request.POST.get('applyfilters', '')
        nofilters = request.POST.get('nofilters', '')
        language = request.POST.get('language', '')
        if search:
            return redirect('/' + str(lang) + '/products/search/?q=' + searchText)
        elif applyfilters:
            pricefilter = request.POST.get('pricefilter', '')
            availablefilter = request.POST.get('availablefilter', '')
            if pricefilter == 'Цена есть' and availablefilter == 'Есть':
                filteredProducts = Продукт.objects.exclude(цена=None).exclude(наличие='-').filter(название_позиции__icontains = q.lower())#| Продукт.objects.exclude(наличие='-') | Продукт.objects.exclude(цена='None')
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'yes',
                    'available': 'yes',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цена есть' and availablefilter == 'Нету':
                filteredProducts = Продукт.objects.exclude(цена=None).filter(наличие='-').filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'yes',
                    'available': 'no',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цены нет' and availablefilter == 'Нету':
                filteredProducts = Продукт.objects.filter(цена=None).filter(наличие='-').filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'no',
                    'available': 'no',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цены нет' and availablefilter == '':
                filteredProducts = Продукт.objects.filter(цена=None).filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'no',
                    'available': 'spec',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == 'Цена есть' and availablefilter == '':
                filteredProducts = Продукт.objects.exclude(цена=None).filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'lang': lang,
                    'withprice': 'yes',
                    'available': 'spec',
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == '' and availablefilter == 'Нету':
                filteredProducts = Продукт.objects.filter(наличие='-').filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'spec',
                    'available': 'no',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == '' and availablefilter == 'Есть':
                filteredProducts = Продукт.objects.exclude(наличие='-').filter(название_позиции__icontains = q.lower())
                context = {
                    'продукты': filteredProducts,
                    'page': int(page),
                    'withprice': 'spec',
                    'available': 'yes',
                    'lang': lang,
                        }
                template = str(lang) + '/products/search/index.html'
                return render(request, template, context)
            elif pricefilter == '' and availablefilter == '':
                context = {
                'продукты': a,
                'page': int(page),
                'withprice': 'spec',
                'available': 'spec',
                'lang': lang,
                    }
            template = str(lang) + '/products/search/index.html'
            return render(request, template, context)
        elif nofilters:
            context = {
                'продукты': a,
                'page': int(page),
                'withprice': 'spec',
                'available': 'spec',
                'lang': lang,
                    }
            template = str(lang) + '/products/search/index.html'
            return render(request, template, context)
        elif language:
            return redirect('/' + str(language))
            
    else:
        template = str(lang) + '/products/search/index.html'
        if len(a) == len(Продукт.objects.all()):
            if lang == 'ru':
                context = {
                    #'продукты': a[0:len(a):],
                    'error_message': 'Пустой запрос',
                    'lang': lang,
                    #'page': int(page),
                    }
                return render(request, template, context)
            elif lang == 'en':
                context = {
                #'продукты': a[0:len(a):],
                'error_message': 'Empty search field',
                'lang': lang,
                #'page': int(page),
                }
            return render(request, template, context)
        elif len(a) == 0:
            if lang == 'ru':
                context = {
                #'продукты': a[0:len(a):],
                'error_message': 'По Вашему запросу ничего не найдено',
                'lang': lang,
                #'page': int(page),
                }
                return render(request, template, context)
            elif lang == 'en':
                context ={
                    #'продукты': a[0:len(a):],
                    'error_message': 'No results were found for your search',
                    'lang': lang,
                    #'page': int(page),
                    }
                return render(request, template, context)                
        else:
            context = {
                'продукты': a[0:len(a):],
                'withprice': 'spec',
                'available': 'spec',
                'lang': lang,
                #'page': int(page),
                }
            return render(request, template, context)

def error404(request, exception):
    return render(request, 'ru/404.html')

def achievementsPage(request, lang):
    language = request.POST.get('language', '')
    if request.POST:
        if language:
            return redirect('/' + str(language))
        else: 
            HttpResponse('404')
    else:
        context = {
            'lang': lang,
        }
        return render(request, str(lang) + '/achievements/index.html', context=context)

def aboutUsPage(request, lang):
    language = request.POST.get('language', '')
    if request.POST:
        if language:
            return redirect('/' + str(language))
        else:
            HttpResponse('404')
    else:
        context = {
            'lang': lang,
        }
        return render(request, str(lang) + '/about/index.html', context=context)


def aboutProductPage(request, id, lang):

    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=90, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)
        admin_order_item = models.CharField(max_length=100, null=True, blank=True)

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
        
    '''for i in продукты:
        if int(i.id) > 47:
            russian_desc = i.описание
            from googletrans import Translator
            translator = Translator(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
            english_desc = translator.translate(russian_desc, dest='en').text
            import time
            time.sleep(2)
            eng_name = translator.translate(i.название_позиции, dest='en').text
            time.sleep(2)
            print(english_desc + ' $ ' + eng_name)
            item = Продукт.objects.get(id=i.id)
            item.description = english_desc
            item.name = eng_name
            item.save()
            print(i.id)'''
        
    favourites = ShopFavourite.objects.all()
    if request.POST:
        cart_add = request.POST.get('add_to_cart', '')
        favourite_add = request.POST.get('add_to_favourite', '')
        first_name = request.POST.get('callme_first_name', '')
        last_name = request.POST.get('callme_last_name', '')
        phone_number = request.POST.get('callme_phone_number')
        callme = request.POST.get('callme_inp_button', '')
        language = request.POST.get('language', '')
        if cart_add:
            item_id = request.POST.get('add_id', '')
            item_name = request.POST.get('add_name', '')
            item_price = request.POST.get('add_price', '')
            default_name = request.POST.get('default_name', '')
            item_currency = request.POST.get('add_currency', '')
            howMuchToAdd = request.POST.get('how_much_to_add', '')
            ToSave = ShopCarty(user_id=request.user.id, item=item_id, name=item_name, price=max(float(i) for i in item_price.replace(',','.').split()), currency=item_currency, admin_order_item=default_name)
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
            return redirect('/' + str(lang) + '/accounts/' + str(request.user.id) + '/cart')
        elif language:
            return redirect('/' + str(language))
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
            return redirect('/' + str(lang) + '/accounts/'+ str(request.user.id) +'/favourites')
        elif callme:
            item_name = request.POST.get('add_name', '')
            item_price = request.POST.get('add_price', '')
            item_currency = request.POST.get('add_currency', '')
            call = ShopCalls(first_name=first_name, last_name=last_name, phone_number=phone_number, timedate=datetime.now(), viewed_product=item_name, price=item_price + ' ' + item_currency)
            call.save()
            return redirect('/' + str(lang) + '/products')  
    else:
        if request.user.is_authenticated == False:
            auth_status = 'failed'
            product = Продукт.objects.get(id=int(id))
            context = {
                'продукт': product,
                'user_id': request.user.id,
                'auth_status': auth_status,
                'lang': lang,
            }
        else: 
            user = AuthUser.objects.get(id=request.user.id)
            auth_status = 'success'
            product = Продукт.objects.get(id=int(id))
            images = product.images.all()
            context = {
                'продукт': product,
                'user_id': request.user.id,
                'user': user,
                'auth_status': auth_status,
                'images': images,
                'lang': lang,
            }
        template = str(lang) + '/productInfo/more.html'
        context.update(csrf(request))
        return render(request, template, context)

def goWithLanguage(request):
    return redirect('/uk')
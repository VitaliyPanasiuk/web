from re import template
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.template.context_processors import csrf
from .models import AuthUser, OrderItem, Products, ShopCurrency, ShopFavourite, Orders
from django.db import models
from django.db.models import F
from django.contrib import messages
import requests
from django.db.utils import IntegrityError
import pytz
from bs4 import BeautifulSoup as bs
import datetime
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime, timezone
products = Products.objects.all()
accounts = AuthUser.objects.all()
timezona = pytz.timezone('Europe/Kiev')

def register(request, lang):
    args = {}
    args.update(csrf(request))
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        username = request.POST.get("username", "")
        email = request.POST.get('email', '')
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        language = request.POST.get('language', '')
        d = datetime.now(pytz.timezone('Europe/Kiev'))
        upper_case = 0
        number = 0
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/register/')
            else:
                return redirect('/' + str(language) + '/accounts/register/')
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        for i in password2:
            if i.isupper():
                upper_case += 1
            elif i.isdigit():
                number += 1
        if password1 == password2:
            if len(password2) >= 8:
                if number > 0 and upper_case > 0:
                            try:
                                user = AuthUser(username=username, password=make_password(password2, salt=None, hasher='default'), email=email, last_login=d, date_joined=d, is_superuser=0, is_staff=0, is_active=1, user_language=lang)
                                user.save()
                                usery = auth.authenticate(username=username, password=password2)
                                auth.login(request, usery)
                                return redirect('/'+ str(lang) + "/accounts/"+str(user.id))
                            except IntegrityError:
                                if lang == 'ru':
                                    error_code = 'Пользователь с таким именем уже существует'
                                    return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                                elif lang == 'en':  
                                    error_code = 'User with this username  already exist'
                                    return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                                elif lang == 'uk':  
                                    error_code = "Користувач з таким ім'ям вже існує"
                                    return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})    
                else:
                    if lang == 'en':
                        error_code = 'Your password must contain at least one number and one capital letter'
                        return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                    elif lang == 'ru':
                        error_code = 'Ваш пароль должен сожержать хотя бы одну цифру и одну заглавную букву'
                        return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                    elif lang == 'uk':
                        error_code = 'Ваш пароль повинен містити хоча б одну цифру та одну велику літеру'
                        return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
            else:
                if lang == 'ru':
                    error_code = 'Ваш пароль слишком короткий'
                    return render(request,str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                elif lang == 'en':
                    error_code = 'Your password is too short'
                    return render(request,str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
                elif lang == 'uk':
                    error_code = 'Ваш пароль дуже короткий'
                    return render(request,str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
        else:
            if lang == 'ru':
                error_code = 'Пароли не совпадают'
                return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
            elif lang == 'en':
                error_code = 'Passwords are different'
                return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})
            elif lang == 'uk':
                error_code = 'Паролі не співпадають'
                return render(request, str(lang) + "/accounts/auth/register.html", {'error_code': error_code,})

    else:
        return render(request, str(lang) + "/accounts/auth/register.html", args)
    '''if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/auth/register.html', {'form': form})'''
    
def login(request, lang):
    args = {}
    args.update(csrf(request))
    if request.POST:
        login = request.POST.get('login', '')
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        language = request.POST.get('language', '')
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        #user = auth.authenticate(username=username, password=password)
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/login/')
            else:
                return redirect('/' + str(language) + '/accounts/login/')
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif login:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                current_user = AuthUser.objects.get(id=request.user.id)
                if current_user.user_language != None:
                    return redirect("/" + current_user.user_language)
                else:
                    return redirect("/uk")
            else:
                if lang == 'en':
                    args["login_error"] = "Wrong username or password!"
                elif lang == 'ru':
                    args['login_error'] = 'Неверное имя пользователя или пароль'
                elif lang == 'uk':
                    args['login_error'] = "Невірне ім'я користувача або пароль"
                return render(request, '' + str(lang) + "/accounts/auth/login.html", args)

    else:
        return render(request, '' + str(lang) + "/accounts/auth/login.html", args)


def logout(request, lang):
    auth.logout(request)
    return redirect("/" + str(lang))


def userProfilePage(request, uid, lang):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    if request.POST:
        language = request.POST.get('language', '')
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid))
            else:
                return redirect('/' + str(language) + '/accounts/' + str(uid))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
    else:        
        context = {
            'auth_status': auth_status,
            "userId": str(request.user.id),
            "account": str(uid),
            'currentUser': AuthUser.objects.get(id=request.user.id)
        }
        template = str(lang) + "/accounts/profilePage/profilePage.html"
        return render(request, template, context)


def userOrders(request, uid, lang):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        itemToDelete = request.POST.get("delete", "")
        language = request.POST.get('language', '')
        if itemToDelete:
            Orders.objects.filter(id=int(itemToDelete)).delete()
            return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/orders')
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/orders')
    else:
        a = Orders.objects.all()
        orders=[]
        for i in a:
            if str(i.user_id) == str(request.user.id):
                orders.append(i)
        orders.reverse()
        context = {
            'auth_status': auth_status,
            "userId": str(request.user.id),
            "account": str(uid),
            "orders": Orders.objects.filter(user_id=request.user.id).order_by('-id'),
            'ordersamount': len(Orders.objects.filter(user_id=request.user.id)), 
        }
        template = lang +  "/accounts/profilePage/orders.html"
        return render(request, template, context)

now = datetime.now(pytz.timezone('Europe/Kiev'))

def userCart(request, uid, lang):
    template = lang + "/accounts/profilePage/cart.html"
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    # ADD TO CART
    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)
        ru_order_item = models.CharField(max_length=500, null=True, blank=True)
        uk_order_item = models.CharField(max_length=500, null=True, blank=True)
        en_order_item = models.CharField(max_length=500, null=True, blank=True)
        image = models.CharField(max_length=200, null=True, blank=True)

        class Meta:
            managed = False
            db_table = "shop_cart"
    summary = 0
    carts = ShopCarty.objects.all()
    cartItems = carts[0 : len(carts):]
    for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                currentItem = Products.objects.get(id=int(cartItem.item))
                if currentItem.скидка > 0:
                    if cartItem.price != currentItem.цена:
                        cartItem.price = currentItem.цена * (1 - (currentItem.скидка/100))
                        cartItem.save()
                else:
                    if cartItem.price != currentItem.цена:
                        cartItem.price = currentItem.цена
                        cartItem.save()
    
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        #itemToDelete = request.POST.get("delete", "")
        itemToDelete = request.POST.get("itemToDelete", "")
        delete = request.POST.get('delete', '')
        addOneMore = request.POST.get("plus", "")
        removeOneMore = request.POST.get("minus", "")
        makeorder = request.POST.get('makeorder', '')
        language = request.POST.get('language', '')
        if addOneMore:
            item = request.POST.get("item_plus", "")
            product = Products.objects.get(id=item)
            carts = ShopCarty.objects.get(item=item)
            carts.amount += 1
            if carts.amount >= int(round(product.минимальный_заказ_опт, 0)):
                carts.price = product.оптовая_цена
            carts.save()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/cart")
        elif removeOneMore:
            item = request.POST.get("item_minus", "")
            product = Products.objects.get(id=item)
            carts = ShopCarty.objects.get(item=item)
            carts.amount -= 1
            if product.скидка > 0:
                if carts.amount < int(round(product.минимальный_заказ_опт, 0)):
                    carts.price = product.цена * (1- (product.скидка/100))
            else: 
                if carts.amount < int(round(product.минимальный_заказ_опт, 0)):
                    carts.price = product.цена
            if carts.amount < product.минимальный_объем_заказа:
                if lang == 'ru':
                    messages.error(request, "Количество товара не может быть меньше " + str(product.минимальный_объем_заказа))
                elif lang == 'en':
                    messages.error(request, "Amount can't be lower than " + str(product.минимальный_объем_заказа))
                elif lang == 'uk':
                    messages.error(request, "Кількість товару не може бути менше " + str(product.минимальный_объем_заказа))
                return redirect('/' + lang +"/accounts/" + str(request.user.id) + "/cart")
            if carts.amount == 0:
                if lang == 'ru':
                    messages.error(request, "Количество товара не может быть меньше 1")
                elif lang == 'en':
                    messages.error(request, "Amount can't be lower than 1")
                elif lang == 'uk':
                    messages.error(request, "Кількість товару не може бути менше 1")
                return redirect('/' + lang +"/accounts/" + str(request.user.id) + "/cart")
            else:
                carts.save()
                return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/cart")
        elif delete:
            ShopCarty.objects.filter(item=itemToDelete).delete()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/cart")
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/cart')
        elif makeorder:
            b = 0
            userAccount = AuthUser.objects.get(id=request.user.id)
            userCarts = ShopCarty.objects.all()
            currencys = ShopCurrency.objects.all()
            needed = currencys[len(currencys) - 1]
            currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
            a = []
            bob = []
            c=[]
            e=[]
            f=[]
            special=[]
            d = datetime.now(pytz.timezone('Europe/Kiev'))
            for i in userCarts:
                if str(i.user_id) == str(request.user.id):
                    b += 1
            if b == 0:
                if lang == 'ru':
                    return HttpResponse('Корзина пуста!')#Have to add speial error message for this situation
                if lang == 'en':
                    return HttpResponse('Empty cart!')
                if lang == 'uk':
                    return HttpResponse('Пустий кошик!')
            else:
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        a.append(str(i.name))
                        if i.currency == 'UAH':
                            c.append(str(i.ru_order_item) + '  Количество: ' + str(i.amount) + 'шт.' + '  Цена: '  + str(round(float(i.price) * float(i.amount), 2)) +  ' UAH' + '\n\n')
                            e.append(str(i.en_order_item) + ' Amount: ' + str(i.amount) + '  Price: '  + str(round(float(i.price) * float(i.amount), 2)) +  ' UAH' + '\n\n')
                            f.append(str(i.uk_order_item) + ' Кількість: ' + str(i.amount) + 'шт.' + ' Ціна: '  + str(round(float(i.price) * float(i.amount), 2)) +  ' UAH' + '\n\n')

                        else:
                            c.append(str(i.ru_order_item) + ',  Количество: ' + str(i.amount) + 'шт.' + '  Цена: '  + str(round(float(i.price) * float(currency) * float(i.amount), 2)) +  ' UAH' + '\n\n')
                            e.append(str(i.en_order_item) + ' Amount: ' + str(i.amount) + '  Price: '  + str(round(float(i.price) * float(currency) * float(i.amount), 2)) +  ' UAH' + '\n\n')
                            f.append(str(i.uk_order_item) + ' Кількість: ' + str(i.amount) + 'шт.' + ' Ціна: '  + str(round(float(i.price) * float(currency) * float(i.amount), 2)) +  ' UAH' + '\n\n')
                for i in a:
                    local = ShopCarty.objects.get(name=i)
                    if local.currency == 'UAH':
                        bob.append(round(float(local.price) * float(local.amount), 2))
                    else:
                        bob.append(round(float(local.price) * currency * float(local.amount), 2))
                intbob = [float(elem) for elem in bob]
                newa = str(a)
                ordery_ru = " ".join(str(x) for x in c)
                ordery_en = " ".join(str(x) for x in e)
                ordery_uk = " ".join(str(x) for x in f)
                order = Orders(
                    user_id=request.user.id,
                    first_name=userAccount.first_name,
                    last_name=userAccount.last_name,
                    order_date=d,
                    email=userAccount.email, 
                    order_price=sum(intbob), 
                    phone_number=userAccount.phone_number, 
                    currency='UAH', 
                    order=ordery_uk, 
                    payment_status='np', 
                    order_status='nd', 
                    confirm='unc', 
                    order_uk=ordery_uk, 
                    order_ru=ordery_ru, 
                    order_en=ordery_en)
                
                order.save()
                
                temp = Orders.objects.filter(user_id = request.user.id).last()

                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        orderItem = OrderItem(
                            name_uk = i.uk_order_item,
                            name_en = i.en_order_item,
                            name_ru = i.ru_order_item,
                            amount = i.amount,
                            price = round(float(i.price) * float(currency) * float(i.amount), 2),
                            order = temp
                        )
                        orderItem.save()
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        i.delete()
            return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/make-order')
    else:


        currencys = ShopCurrency.objects.all()
        needed = currencys[len(currencys) - 1]
        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
        carts = ShopCarty.objects.all()
        cartItems = carts[0 : len(carts):]
        a = []
        b = []
        c = []
        for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                currentItem = Products.objects.get(id=int(cartItem.item))
                if currentItem.скидка > 0:
                    if cartItem.price != currentItem.цена:
                        cartItem.price = currentItem.цена * (1 - (currentItem.скидка/100))
                        cartItem.save()
                else:
                    if cartItem.price != currentItem.цена:
                        cartItem.price = currentItem.цена
                        cartItem.save()
                
        for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                a.append(cartItem.name)
                b.append(cartItem.amount)
                c.append(cartItem)
            
        for i in carts:
            if int(i.user_id) == request.user.id:
                if i.currency == 'UAH':
                    local_sum = round(float(i.price) * float(i.amount), 2)
                elif i.currency == 'USD':
                    local_sum = round(float(i.price) * float(i.amount) * float(currency), 2)
                summary += local_sum
        try:
            context = {
                
                'auth_status': auth_status,
                "items": c,
                "amounts": b,
                "userId": str(request.user.id),
                "account": str(uid),
                "sum": round(summary, 2),
                'currency': currency,
            }
        except UnboundLocalError:
            context = {
            'auth_status': auth_status,
            "items": c,
            "amounts": b,
            "userId": str(request.user.id),
            "account": str(uid),
            "sum": summary,
            'currency': currency,
        }
        context.update(csrf(request))
        return render(request, template, context)


def userFavourites(request, uid, lang):
    template = lang + "/accounts/profilePage/favourites.html"
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'

    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        itemToDelete = request.POST.get("delete", "")
        language = request.POST.get('language', '')
        if itemToDelete:
            ShopFavourite.objects.filter(favourite_item=itemToDelete).delete()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/favourites")
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/favourites')
    else:
        favourites = ShopFavourite.objects.all()
        a = []
        for i in favourites:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
        #print(len(ShopFavourite.objects.filter(user_id=request.user.id)))
        context = {
            'auth_status': auth_status,
            "favourites": a,
            'userId': str(request.user.id),
            'account': str(uid),
            'items': len(ShopFavourite.objects.filter(user_id=request.user.id)),
        }
        context.update(csrf(request))
        return render(request, template, context)

def deleteAccount(request, lang):
    template = lang + "/accounts/auth/delete.html"
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        yes = request.POST.get("yes", "")
        no = request.POST.get("no", "")
        language = request.POST.get("language", "")
        if yes:
            password = request.POST.get("password", "")
            current_user = AuthUser.objects.get(id=request.user.id)
            if password == "":
                if lang == 'ru':
                    context = {
                    "error_message": "Пустое поле пароль. Попробуйте снова"
                    }
                elif lang == 'en':
                    context = {
                    "error_message": "Empty password field. Try again"
                    }
                elif lang == 'uk':
                    context = {
                    "error_message": "Пусте поле паролю. Попробуйте знову"
                    }
                return render(request, template, context)
            if check_password(password=password , encoded=current_user.password) == True:
                current_user.delete()
                return redirect("/" + lang)
            else:
                if lang == 'ru':
                    context = {
                    "error_message": "Вы ввели неправильный пароль. Попробуйте снова"
                    }
                elif lang == 'en':
                    context = {
                    "error_message": "You entered wrong password. Try again"
                    }
                elif lang == 'uk':
                    context = {
                    "error_message": "Ви ввели неправильний пароль. Попробуйте знову"
                    }
                return render(request, template, context)
                
        elif no:
            return redirect("/" + lang + "/accounts/" + str(request.user.id))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/delete')
    else:
        
        return render(request, template)

def editProfilePage(request, uid ,lang):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    new_name = request.POST.get('new_name', '')
    new_last_name = request.POST.get('new_last_name', '')
    new_email = request.POST.get('new_email', '')
    new_phonenumber = request.POST.get('new_phonenumber', '')
    new_city = request.POST.get('new_city', '')
    new_street = request.POST.get('new_street', '')
    new_house = request.POST.get('new_house', '')
    password = request.POST.get('password', '')
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        userProfile = AuthUser.objects.get(id=uid)
        language = request.POST.get('language', '')
        userProfile.first_name = new_name
        userProfile.last_name = new_last_name
        userProfile.email = new_email
        userProfile.phone_number = new_phonenumber
        userProfile.city = new_city
        userProfile.street = new_street
        userProfile.house = new_house
        if check_password(password=password, encoded=userProfile.password) == True:
            userProfile.save()
            return redirect('/' + lang + '/accounts/'+ str(uid))
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/edit')
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        else:
            template = lang + '/accounts/editProfile/edit.html'
            if lang == 'ru':
                context = {
                    'error_message': 'Неправильный пароль',
                }
            elif lang == 'uk':
                context = {
                'error_message': 'Неправильний пароль',
                }
            elif lang == 'en':
                context = {
                'error_message': 'Wrong password',
                }
            context.update(csrf(request))
            return render(request, template, context)  
    else:
        userProfile = AuthUser.objects.get(id=uid)
        template = lang + '/accounts/editProfile/edit.html'
        context = {
            'userProfile': userProfile,
        }
        context.update(csrf(request))
        return render(request, template, context)

def editPasswordPage(request, uid, lang):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    old_pwd = request.POST.get('old_pwd', '')
    new_pwd = request.POST.get('new_pwd', '')
    repeat_new_pwd = request.POST.get('repeat_new_pwd', '')
    userProfile = AuthUser.objects.get(id=request.user.id)
    template = lang + '/accounts/editProfile/editPassword.html'
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        language = request.POST.get('language', '')
        if check_password(password=old_pwd , encoded=userProfile.password) == True:
            if new_pwd == repeat_new_pwd:

                upper_case = 0
                number = 0
    
                for i in new_pwd:
                    if i.isupper():
                        upper_case += 1
                    elif i.isdigit():
                        number += 1

                if number > 0 and upper_case > 0:
                    username = userProfile.username
                    hashed_pwd = make_password(repeat_new_pwd, salt=None, hasher='default')
                    userProfile.password = hashed_pwd
                    userProfile.save()
                    user = auth.authenticate(username=username, password=repeat_new_pwd)
                    auth.login(request, user)
                    return redirect('/' + lang + '/accounts/'+ str(uid))
                else:
                    if lang == 'ru':
                        error_code = 'Ваш пароль должен сожержать хотя бы одну цифру и одну заглавную букву'
                    elif lang == 'en':
                        error_code = 'Your password must contain at least one number and one capital letter'
                    elif lang == 'uk':
                        error_code = 'Ваш пароль повинен містити хоча б одну цифру та одну велику літеру'
                    context = {
                    'error_message': error_code,
                }
                return render(request, template, context)

            else:
                if lang == 'ru':
                    error_code = 'Новые пароли не совпадают. Повторите попытку'
                elif lang == 'en':
                    error_code = 'New passwords are different. Try again'
                elif lang == 'uk':
                    error_code = 'Нові паролі не співпадають. Спробуйте ще раз'
                context = {
                'error_message': error_code,
            }
            return render(request, template, context)
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/change-password')
        else:
            if lang == 'ru':
                error_code = 'Неверный старый пароль. Попробуйте снова'
            elif lang == 'en':
                error_code = 'Wrong old password. Try again'
            elif lang == 'uk':
                error_code = 'Невірний старий пароль. Спробуйте ще раз'
            context = {
                'error_message': error_code,
            }
            return render(request, template, context)
    else:
        template = lang + '/accounts/editProfile/editPassword.html'
        return render(request, template)

def makeOrder(request, uid, lang):
    if request.user.is_authenticated == False:
        auth_status = 'failed'
        return HttpResponse('404')
    else: 
        auth_status = 'success'
    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)
        en_order_item = models.CharField(max_length=500, blank=True, null=True)
        ru_order_item = models.CharField(max_length=500, blank=True, null=True)
        uk_order_item = models.CharField(max_length=500, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_cart"

    if request.user.is_anonymous:
        anon = True
    template = lang + '/accounts/profilePage/makingOrder.html'
    try:
        user = AuthUser.objects.get(id=str(request.user.id))
    except ValueError:
        user = AuthUser.objects.get(id=str(1))
    cart = ShopCarty.objects.all()
    orders= Orders.objects.all()
    a = []
    price = 0
    currencys = ShopCurrency.objects.all()
    needed = currencys[len(currencys) - 1]
    currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        language = request.POST.get('language', '')
        go = request.POST.get('go', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        orderFromHtml = request.POST.get('order', '')
        priceFromHtml = request.POST.get('price', '')
        typeOfDelivery = request.POST.get('typeOfDelivery', '')
        typeOfPayment = request.POST.get('typeOfPayment', '')
        city = request.POST.get('city', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        ukr_pochta = request.POST.get('ukr_pochta', '')
        nova_pochta = request.POST.get('nova_pochta', '')
        #normalPrice = max(float(i) for i in priceFromHtml.replace(',','.').split())
        if language:
            last_order = Orders.objects.filter(user_id=request.user.id).last()
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/edit-order/' + str(last_order.id))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        if orderFromHtml == None:
            for i in cart:
                if str(i.user_id) == str(request.user.id):
                    a.append(i)
                    if i.currency == 'UAH':
                        price += round(float(i.price) * float(i.amount), 2)
                    else:
                        currencys = ShopCurrency.objects.all()
                        needed = currencys[len(currencys) - 1]
                        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                        price += round(float(i.price) * float(currency) * float(i.amount), 2)
            '''b = max(a)
            newUser = ShopCarty.objects.get(cart_id=b)'''
            if lang == 'ru':
                error_message = 'Ошибка: Пустой заказ'
            elif lang == 'en':
                error_message = 'Error: Empty order'
            elif lang == 'uk':
                error_message = 'Помилка: Порожнє замовлення'
            context = {
                'currency': currency,
                'auth_status': auth_status,
                'user': user,
                'userCart': a,
                'price': price,
                'userId': str(request.user.id),
                'account': str(uid),
                'error_message': error_message
            }
            return render(request, template, context)
        if (street == 'None'or house == 'None' or city == 'None') and typeOfDelivery != 'Самовывоз':
            for i in cart:
                if str(i.user_id) == str(request.user.id):
                    a.append(i)
                    if i.currency == 'UAH':
                        price += round(float(i.price) * float(i.amount), 2)
                    else:
                        currencys = ShopCurrency.objects.all()
                        needed = currencys[len(currencys) - 1]
                        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                        price += round(float(i.price) * float(currency) * float(i.amount), 2)
            '''b = max(a)
            newUser = ShopCarty.objects.get(cart_id=b)'''
            if lang == 'ru':
                error_message = 'Ошибка: Введите корректный адрес'
            elif lang == 'en':
                error_message = 'Error: Enter correct address'
            elif lang == 'uk':
                error_message = 'Помилка: Введіть правильну адресу'
            context = {
                'currency': currency,
                'auth_status': auth_status,
                'user': user,
                'userCart': a,
                'price': price,
                'userId': str(request.user.id),
                'account': str(uid),
                'error_message': error_message,
            }
            return render(request, template, context)
        if go:
            if typeOfDelivery == 'Самовывоз':
                #d = datetime.now(pytz.timezone('Europe/Kiev'))
                userCarts = ShopCarty.objects.all()
                specorder = Orders.objects.last()
                specorder.first_name = first_name
                specorder.last_name = last_name
                specorder.email = email
                specorder.phone_number = phone_number
                specorder.city = ''
                specorder.street = ''
                specorder.house = ''
                specorder.delivery_type = typeOfDelivery
                specorder.payment_type = typeOfPayment
                specorder.nova_pochta = ''
                specorder.ukr_pochta = ''
                specorder.confirm = 'uc'
                specorder.save()
            else:
                #d = datetime.now(pytz.timezone('Europe/Kiev'))
                userCarts = ShopCarty.objects.all()
                specorder = Orders.objects.last()
                specorder.first_name = first_name
                specorder.last_name = last_name
                specorder.email = email
                specorder.phone_number = phone_number
                specorder.city = city
                specorder.street = street
                specorder.house = house
                specorder.delivery_type = typeOfDelivery
                specorder.payment_type = typeOfPayment
                specorder.nova_pochta = nova_pochta
                specorder.ukr_pochta = ukr_pochta
                specorder.confirm = 'uc'
                specorder.save()
            for i in userCarts:
                if str(i.user_id) == str(request.user.id):
                    i.delete()
            if typeOfPayment == 'Наличный':
                '''toDelete = Orders.objects.last()
                toDelete.delete()'''
                return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/orders')
            else:
                '''toDelete = Orders.objects.last()
                toDelete.delete()'''
                return redirect('/payment')
    else:
        for i in cart:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
                if i.currency == 'UAH':
                    price += round(float(i.price) * float(i.amount), 2)
                else:
                    currencys = ShopCurrency.objects.all()
                    needed = currencys[len(currencys) - 1]
                    currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                    price += round(float(i.price) * float(currency) * float(i.amount), 2)
        '''b = max(a)
        newUser = ShopCarty.objects.get(cart_id=b)'''
        context = {
            'auth_status': auth_status,
            'user': user,
            'userCart': a,
            'price': price,
            'userId': str(request.user.id),
            'account': str(uid),
            'currency': currency
        }
        return render(request, template, context)

def orderInfo(request, oid, uid, lang):
    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)
        en_order_item = models.CharField(max_length=500, blank=True, null=True)
        ru_order_item = models.CharField(max_length=500, blank=True, null=True)
        uk_order_item = models.CharField(max_length=500, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_cart"

    if request.user.is_authenticated == False:
            auth_status = 'failed'
            return HttpResponse('404')
    else: 
        auth_status = 'success'
        
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        edit = request.POST.get('edit', '')
        editid = request.POST.get('editid', '')
        language = request.POST.get('language', '')
        if edit:
            return redirect('/' + lang + '/accounts/'+str(request.user.id)+'/edit-order/'+str(editid))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/order/' + str(oid))
    else:
        try:
            user = AuthUser.objects.get(id=str(request.user.id))
        except ValueError:
            user = AuthUser.objects.get(id=str(1))
        template = lang + '/accounts/orderInfo/order.html'
        cart = ShopCarty.objects.all()
        orders = Orders.objects.all()
        a = []
        price = 0
        order = Orders.objects.get(id=str(oid))
        needed = ShopCurrency.objects.last()
        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
        context = {
            'order': order,
            'user': user,
            'auth_status': auth_status,
            'currency': currency,
            }
        return render(request, template, context)

def success_order(request, uid, lang):
    if request.user.is_authenticated == False:
        auth_status = 'failed'
        return HttpResponse('404')
    else: 
        auth_status = 'success'
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        language = request.POST.get('language', '')
        if language:
            current_user = AuthUser.objects.get(id=request.user.id)
            current_user.user_language = str(language)
            current_user.save()
            return redirect('/' + str(language))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
    else:
        template = lang + '/accounts/profilePage/success.html'
        context = {
            'auth_status': auth_status,
        }
        return render(request, template, context)

def edit_order_page(request, uid, oid, lang):
    template = lang + '/accounts/editOrder/editOrder.html'
    if request.user.is_authenticated == False:
        auth_status = 'failed'
        return HttpResponse('404')
    else: 
        auth_status = 'success'
    try:
        user = AuthUser.objects.get(id=str(request.user.id))
    except ValueError:
        user = AuthUser.objects.get(id=str(1))
    if request.POST:
        search = request.POST.get("search", "")
        searchTextRaw = request.POST.get("searchtext", "")
        searchText = searchTextRaw.replace(" ", "-")
        language = request.POST.get('language', '')
        go = request.POST.get('go', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        orderFromHtml = request.POST.get('order', '')
        priceFromHtml = request.POST.get('price', '')
        typeOfDelivery = request.POST.get('typeOfDelivery', '')
        typeOfPayment = request.POST.get('typeOfPayment', '')
        city = request.POST.get('city', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        ukr_pochta = request.POST.get('ukr_pochta', '')
        nova_pochta = request.POST.get('nova_pochta', '')
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/edit-order/' + str(oid))
        elif search:
            return redirect("/" + str(lang) + "/products/search/?q=" + searchText)
        if orderFromHtml == None:
            if lang == 'ru':
                error_message = 'Ошибка: Пустой заказ'
            elif lang == 'en':
                error_message = 'Error: Empty order'
            elif lang == 'uk':
                error_message = 'Помилка: Порожнє замовлення'
            context = {
                'auth_status': auth_status,
                'userId': str(request.user.id),
                'user': user,
                'error_message': error_message
            }
            return render(request, template, context)
        
        if (street == 'None'or house == 'None' or city == 'None') and typeOfDelivery != 'Самовывоз':
            if lang == 'ru':
                error_message = 'Ошибка: Введите корректный адрес'
            elif lang == 'en':
                error_message = 'Error: Enter correct address'
            elif lang == 'uk':
                error_message = 'Помилка: Введіть правильну адресу'
            context = {
                'auth_status': auth_status,
                'user': user,
                'userId': str(request.user.id),
                'account': str(uid),
                'error_message': error_message,
            }
            return render(request, template, context)
        if go:
            if typeOfDelivery == 'Самовывоз':
                #d = datetime.now(pytz.timezone('Europe/Kiev'))
                specorder = Orders.objects.get(id=int(oid))
                specorder.first_name = first_name
                specorder.last_name = last_name
                specorder.email = email
                specorder.phone_number = phone_number
                specorder.city = ''
                specorder.street = ''
                specorder.house = ''
                specorder.delivery_type = typeOfDelivery
                specorder.payment_type = typeOfPayment
                specorder.nova_pochta = ''
                specorder.ukr_pochta = ''
                specorder.confirm = 'uc'
                specorder.save()
            else:
                #d = datetime.now(pytz.timezone('Europe/Kiev'))
                specorder = Orders.objects.get(id=int(oid))
                specorder.first_name = first_name
                specorder.last_name = last_name
                specorder.email = email
                specorder.phone_number = phone_number
                specorder.city = city
                specorder.street = street
                specorder.house = house
                specorder.delivery_type = typeOfDelivery
                specorder.payment_type = typeOfPayment
                specorder.nova_pochta = nova_pochta
                specorder.ukr_pochta = ukr_pochta
                specorder.confirm = 'uc'
                specorder.save()
            if typeOfPayment == 'Наличный':
                return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/success-order')
            else:
                return redirect('/payment')
    else:
        
        order = Orders.objects.get(id=int(oid))
        context = {
            'auth_status': auth_status,
            'user': user,
            'order': order,
        }
        return render(request, template, context)
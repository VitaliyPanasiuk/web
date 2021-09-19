from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.template.context_processors import csrf
from .models import AuthUser, Продукт, ShopCurrency, ShopFavourite
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
products = Продукт.objects.all()
accounts = AuthUser.objects.all()
timezona = pytz.timezone('Europe/Kiev')

def register(request, lang):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        email = request.POST.get('email', '')
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        language = request.POST.get('language', '')
        d = datetime.now(pytz.timezone('Europe/Kiev'))
        upper_case = 0
        lower_case = 0
        number = 0
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/register/')
            else:
                return redirect('/' + str(language) + '/accounts/register/')
        for i in password2:
            if i.isupper():
                upper_case += 1
            elif i.islower():
                lower_case += 1
            elif i.isdigit():
                number += 1
        if password1 == password2:
            if len(password2) >= 8:
                if number > 0 and upper_case > 0:
                            try:
                                user = AuthUser(username=username, password=make_password(password2, salt=None, hasher='default'), email=email, last_login=d, date_joined=d, is_superuser=0, is_staff=0, is_active=1)
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
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        language = request.POST.get('language', '')
        user = auth.authenticate(username=username, password=password)
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/login/')
            else:
                return redirect('/' + str(language) + '/accounts/login/')
        if user is not None:
            auth.login(request, user)
            return redirect("/" + str(lang))
        else:
            if lang == 'en':
                args["login_error"] = "Wrong username or password!"
            elif lang == 'ru':
                args['login_error'] = 'Неверное имя пользователя или пароль'
            elif lang == 'uk':
                args['login_error'] = "Невірне ім'я користувача або пароль"
            return render(request, '' + str(lang) + "/accounts/auth/failed.html", args)

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
        if language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid))
            else:
                return redirect('/' + str(language) + '/accounts/' + str(uid))
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
    class ShopOrdery(models.Model):
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        #order = models.ManyToManyField(Продукт)
        сумма_заказа = models.FloatField(blank=True, null=True)
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
        confirm = models.CharField(max_length=500, blank=True, null=True)
        order_uk = models.TextField(max_length=2000, blank=True, null=True)
        order_ru = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')
        order_en = models.TextField(max_length=2000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'
    if request.POST:
        itemToDelete = request.POST.get("delete", "")
        language = request.POST.get('language', '')
        if itemToDelete:
            ShopOrdery.objects.filter(id=int(itemToDelete)).delete()
            return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/orders')
        elif language:
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/orders')
    else:
        a = ShopOrdery.objects.all()
        orders=[]
        for i in a:
            if str(i.user_id) == str(request.user.id):
                orders.append(i)
        context = {
            'auth_status': auth_status,
            "userId": str(request.user.id),
            "account": str(uid),
            "orders": ShopOrdery.objects.filter(user_id=request.user.id),
            'ordersamount': len(ShopOrdery.objects.filter(user_id=request.user.id)), 
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
    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        user_order = models.CharField(max_length=10000, blank=True, null=True)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
        confirm = models.CharField(max_length=500, blank=True, null=True)
        order_uk = models.TextField(max_length=2000, blank=True, null=True)
        order_ru = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')
        order_en = models.TextField(max_length=2000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

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

        class Meta:
            managed = False
            db_table = "shop_cart"
    summary = 0
    # DELETE FROM CART
    if request.POST:
        itemToDelete = request.POST.get("delete", "")
        addOneMore = request.POST.get("plus", "")
        removeOneMore = request.POST.get("minus", "")
        makeorder = request.POST.get('makeorder', '')
        language = request.POST.get('language', '')
        if addOneMore:
            item = request.POST.get("item_plus", "")
            product = Продукт.objects.get(id=item)
            carts = ShopCarty.objects.get(item=item)
            carts.amount += 1
            if carts.amount >= int(round(product.минимальный_заказ_опт, 0)):
                carts.price = product.оптовая_цена
            carts.save()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/cart")
        elif removeOneMore:
            item = request.POST.get("item_minus", "")
            product = Продукт.objects.get(id=item)
            carts = ShopCarty.objects.get(item=item)
            carts.amount -= 1
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
        elif itemToDelete:
            ShopCarty.objects.filter(item=itemToDelete).delete()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/cart")
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
                            c.append(str(i.ru_order_item) + '  Количество: ' + str(i.amount) + 'шт.' + '  Цена: '  + str(round(int(i.price) * int(i.amount), 2)) +  'UAH' + '\n\n')
                            e.append(str(i.en_order_item) + ' Amount: ' + str(i.amount) + '  Price: '  + str(round(int(i.price) * int(i.amount), 2)) +  'UAH' + '\n\n')
                            f.append(str(i.uk_order_item) + ' Кількість: ' + str(i.amount) + 'шт.' + ' Ціна: '  + str(round(int(i.price) * int(i.amount), 2)) +  'UAH' + '\n\n')

                        else:
                            c.append(str(i.ru_order_item) + ',  Количество: ' + str(i.amount) + 'шт.' + '  Цена: '  + str(round(int(i.price) * currency * int(i.amount), 2)) +  'UAH' + '\n\n')
                            e.append(str(i.en_order_item) + ' Amount: ' + str(i.amount) + '  Price: '  + str(round(int(i.price) * currency * int(i.amount), 2)) +  'UAH' + '\n\n')
                            f.append(str(i.uk_order_item) + ' Кількість: ' + str(i.amount) + 'шт.' + ' Ціна: '  + str(round(int(i.price) * currency * int(i.amount), 2)) +  'UAH' + '\n\n')
                for i in a:
                    local = ShopCarty.objects.get(name=i)
                    if local.currency == 'UAH':
                        bob.append(round(float(local.price) * float(local.amount), 2))
                    else:
                        bob.append(round(float(local.price) * currency * float(local.amount), 2))
                intbob = [float(elem) for elem in bob]
                newa = str(a)
                if lang == 'ru':
                    ordery_ru = " ".join(str(x) for x in c)
                    ordery_en = " ".join(str(x) for x in e)
                    ordery_uk = " ".join(str(x) for x in f)
                    order = ShopOrdery(user_id=request.user.id, имя=userAccount.first_name, фамилия=userAccount.last_name, дата_заказа=d, почта=userAccount.email, сумма_заказа=sum(intbob), телефон=userAccount.phone_number, валюта_заказа='UAH', заказ=ordery_ru, статус_оплаты='np', статус_заказа='nd', confirm='unc', order_uk=ordery_uk, order_ru=ordery_ru, order_en=ordery_en)             
                elif lang == 'en':
                    ordery_ru = " ".join(str(x) for x in c)
                    ordery_en = " ".join(str(x) for x in e)
                    ordery_uk = " ".join(str(x) for x in f)
                    order = ShopOrdery(user_id=request.user.id, имя=userAccount.first_name, фамилия=userAccount.last_name, дата_заказа=d, почта=userAccount.email, сумма_заказа=sum(intbob), телефон=userAccount.phone_number, валюта_заказа='UAH', заказ=ordery_en, статус_оплаты='np', статус_заказа='nd', confirm='unc', order_uk=ordery_uk, order_ru=ordery_ru, order_en=ordery_en)
                elif lang == 'uk':
                    ordery_ru = " ".join(str(x) for x in c)
                    ordery_en = " ".join(str(x) for x in e)
                    ordery_uk = " ".join(str(x) for x in f)
                    order = ShopOrdery(user_id=request.user.id, имя=userAccount.first_name, фамилия=userAccount.last_name, дата_заказа=d, почта=userAccount.email, сумма_заказа=sum(intbob), телефон=userAccount.phone_number, валюта_заказа='UAH', заказ=ordery_uk, статус_оплаты='np', статус_заказа='nd', confirm='unc', order_uk=ordery_uk, order_ru=ordery_ru, order_en=ordery_en)
                order.save()
                '''for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        i.delete()'''
            return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/make-order')
    else:


        '''orders = ShopOrdery.objects.all()
        for order in orders:
            creationTime = order.дата_заказа
                #print(creationTime)
                #print(datetime.now(pytz.timezone('Europe/Kiev')))
            difference = datetime.now(pytz.timezone('Europe/Kiev')) - creationTime
            res = list(str(difference))
            print(res)
            if str(res[0]) != '0' and order.confirm != 'c':
                order.delete()'''


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
                a.append(cartItem.name)
                b.append(cartItem.amount)
                c.append(cartItem)
        for i in carts:
            if int(i.user_id) == request.user.id:
                if i.currency == 'UAH':
                    local_sum = int(i.price) * int(i.amount)
                elif i.currency == 'USD':
                    local_sum = round(int(i.price) * int(i.amount) * currency, 2)
                summary += local_sum
        try:
            context = {
                'auth_status': auth_status,
                "items": c,
                "amounts": b,
                "userId": str(request.user.id),
                "account": str(uid),
                "sum": summary,
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
        itemToDelete = request.POST.get("delete", "")
        language = request.POST.get('language', '')
        if itemToDelete:
            ShopFavourite.objects.filter(favourite_item=itemToDelete).delete()
            return redirect('/' + lang + "/accounts/" + str(request.user.id) + "/favourites")
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
        print(len(ShopFavourite.objects.filter(user_id=request.user.id)))
        context = {
            'auth_status': auth_status,
            "favourites": a,
            'userId': str(request.user.id),
            'account': str(uid),
            'items': len(ShopFavourite.objects.filter(user_id=request.user.id)),
        }
        context.update(csrf(request))
        return render(request, template, context)


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
        language = request.POST.get('language', '')
        if check_password(password=old_pwd , encoded=userProfile.password) == True:
            if new_pwd == repeat_new_pwd:
                username = userProfile.username
                hashed_pwd = make_password(repeat_new_pwd, salt=None, hasher='default')
                userProfile.password = hashed_pwd
                userProfile.save()
                user = auth.authenticate(username=username, password=repeat_new_pwd)
                auth.login(request, user)
                return redirect('/' + lang + '/accounts/'+ str(uid))
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
    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
        confirm = models.CharField(max_length=500, blank=True, null=True)
        order_uk = models.TextField(max_length=2000, blank=True, null=True)
        order_ru = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')
        order_en = models.TextField(max_length=2000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

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
    orders= ShopOrdery.objects.all()
    a = []
    price = 0
    currencys = ShopCurrency.objects.all()
    needed = currencys[len(currencys) - 1]
    currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
    if request.POST:
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
            last_order = ShopOrdery.objects.filter(user_id=request.user.id).last()
            if request.user.id != None:
                current_user = AuthUser.objects.get(id=request.user.id)
                current_user.user_language = str(language)
                current_user.save()
                return redirect('/' + current_user.user_language + '/accounts/' + str(uid) + '/edit-order/' + str(last_order.id))
        if orderFromHtml == None:
            for i in cart:
                if str(i.user_id) == str(request.user.id):
                    a.append(i)
                    if i.currency == 'UAH':
                        price += int(i.price) * int(i.amount)
                    else:
                        currencys = ShopCurrency.objects.all()
                        needed = currencys[len(currencys) - 1]
                        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                        price += int(i.price) * currency * int(i.amount)
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
                        price += int(i.price) * int(i.amount)
                    else:
                        currencys = ShopCurrency.objects.all()
                        needed = currencys[len(currencys) - 1]
                        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                        price += int(i.price) * currency * int(i.amount)
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
                specorder = ShopOrdery.objects.last()
                specorder.имя = first_name
                specorder.фамилия = last_name
                specorder.почта = email
                specorder.телефон = phone_number
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
                specorder = ShopOrdery.objects.last()
                specorder.имя = first_name
                specorder.фамилия = last_name
                specorder.почта = email
                specorder.телефон = phone_number
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
                '''toDelete = ShopOrdery.objects.last()
                toDelete.delete()'''
                return redirect('/' + lang + '/accounts/' + str(request.user.id) + '/orders')
            else:
                '''toDelete = ShopOrdery.objects.last()
                toDelete.delete()'''
                return redirect('/payment')
    else:
        for i in cart:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
                if i.currency == 'UAH':
                    price += int(i.price) * int(i.amount)
                else:
                    currencys = ShopCurrency.objects.all()
                    needed = currencys[len(currencys) - 1]
                    currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                    price += int(i.price) * currency * int(i.amount)
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

    class ShopOrdery(models.Model):
        id = models.IntegerField(db_column='id', primary_key=True, null=False,)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
        confirm = models.CharField(max_length=500, blank=True, null=True)
        order_uk = models.TextField(max_length=2000, blank=True, null=True)
        order_ru = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')
        order_en = models.TextField(max_length=2000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

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
        edit = request.POST.get('edit', '')
        editid = request.POST.get('editid', '')
        language = request.POST.get('language', '')
        if edit:
            return redirect('/' + lang + '/accounts/'+str(request.user.id)+'/edit-order/'+str(editid))
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
        orders = ShopOrdery.objects.all()
        a = []
        price = 0
        order = ShopOrdery.objects.get(id=str(oid))
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
        language = request.POST.get('language', '')
        if language:
            return redirect('/' + str(language))
    else:
        template = lang + '/accounts/profilePage/success.html'
        context = {
            'auth_status': auth_status,
        }
        return render(request, template, context)

def edit_order_page(request, uid, oid, lang):

    class ShopOrdery(models.Model):
        id = models.IntegerField(db_column='id', primary_key=True, null=False,)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)
        confirm = models.CharField(max_length=500, blank=True, null=True)
        order_uk = models.TextField(max_length=2000, blank=True, null=True)
        order_ru = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Заказ')
        order_en = models.TextField(max_length=2000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

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
                specorder = ShopOrdery.objects.get(id=int(oid))
                specorder.имя = first_name
                specorder.фамилия = last_name
                specorder.почта = email
                specorder.телефон = phone_number
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
                specorder = ShopOrdery.objects.get(id=int(oid))
                specorder.имя = first_name
                specorder.фамилия = last_name
                specorder.почта = email
                specorder.телефон = phone_number
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
        
        order = ShopOrdery.objects.get(id=int(oid))
        context = {
            'auth_status': auth_status,
            'user': user,
            'order': order,
        }
        return render(request, template, context)
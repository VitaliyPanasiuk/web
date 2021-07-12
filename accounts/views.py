from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.template.context_processors import csrf
from .models import AuthUser, Продукт, ShopCurrency
from django.db import models
from django.db.models import F
from django.contrib import messages
import requests
import pytz
from bs4 import BeautifulSoup as bs
import datetime
from django.contrib.auth.hashers import check_password, make_password
products = Продукт.objects.all()
accounts = AuthUser.objects.all()
timezone = pytz.timezone('Europe/Kiev')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/auth/register.html', {'form': form})
    '''if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "accounts/auth/register.html", {"form": form})'''


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args["login_error"] = "Wrong username or password!"
            return render(request, "accounts/auth/failed.html", args)

    else:
        return render(request, "accounts/auth/login.html", args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def userProfilePage(request, uid):
    context = {
        "userId": str(request.user.id),
        "account": str(uid),
        'currentUser': AuthUser.objects.get(id=request.user.id)
    }
    template = "accounts/profilePage/profilePage.html"
    return render(request, template, context)


def userOrders(request, uid):
    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=1000, blank=True, null=True)
        сумма_заказа = models.FloatField(blank=True, null=True)
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        адрес_заказа = models.CharField(max_length=90)
        дата_заказа = models.DateTimeField(blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'
    a = ShopOrdery.objects.all()
    orders=[]
    for i in a:
        if str(i.user_id) == str(request.user.id):
            orders.append(i)
    context = {
        "userId": str(request.user.id),
        "account": str(uid),
        "orders": orders,
    }
    template = "accounts/profilePage/orders.html"
    return render(request, template, context)

now = datetime.datetime.now()

def userCart(request, uid):
    template = "accounts/profilePage/cart.html"

    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=45)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        адрес_заказа = models.CharField(max_length=90)
        дата_заказа = models.DateTimeField(blank=True, null=True)

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
        if addOneMore:
            item = request.POST.get("item_plus", "")
            carts = ShopCarty.objects.get(item=item)
            carts.amount += 1
            carts.save()
            return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif removeOneMore:
            item = request.POST.get("item_minus", "")
            carts = ShopCarty.objects.get(item=item)
            carts.amount -= 1
            if carts.amount == 0:
                messages.error(request, "Количество товара не может быть меньше 1")
                return redirect("/accounts/" + str(request.user.id) + "/cart")
            else:
                carts.save()
                return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif itemToDelete:
            ShopCarty.objects.filter(item=itemToDelete).delete()
            return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif makeorder:
            '''b = 0
            userAccount = AuthUser.objects.get(id=request.user.id)
            userCarts = ShopCarty.objects.all()
            currencys = ShopCurrency.objects.all()
            needed = currencys[len(currencys) - 1]
            currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
            a = []
            bob = []
            d = datetime.datetime.now()
            for i in userCarts:
                if str(i.user_id) == str(request.user.id):
                    b += 1
            if b == 0:
                return HttpResponse('your cart is empty!')#Have to add speial error message for this situation
            else:
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        a.append(i.name)
                for i in a:
                    local = ShopCarty.objects.get(name=i)
                    if local.currency == 'UAH':
                        bob.append(round(float(local.price) * float(local.amount), 2))
                    else:
                        bob.append(round(float(local.price) * currency * float(local.amount), 2))
                intbob = [float(elem) for elem in bob]
                order = ShopOrdery(user_id=request.user.id, имя=userAccount.first_name, фамилия=userAccount.last_name, почта=userAccount.email, сумма_заказа=sum(intbob), дата_заказа=d, телефон=userAccount.phone_number, адрес_заказа=userAccount.address, валюта_заказа='UAH', заказ=a, статус_оплаты='np', статус_заказа='nd')
                order.save()
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        i.delete()'''
            return redirect('/accounts/' + str(request.user.id) + '/make-order')
    else:
        currencys = ShopCurrency.objects.all()
        needed = currencys[len(currencys) - 1]
        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
        carts = ShopCarty.objects.all()
        cartItems = carts[0 : len(carts):]
        a = []
        b = []
        for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                a.append(cartItem.name)
                b.append(cartItem.amount)
        for i in carts:
            if int(i.user_id) == request.user.id:
                if i.currency == 'UAH':
                    local_sum = int(i.price) * int(i.amount)
                elif i.currency == 'USD':
                    local_sum = round(int(i.price) * int(i.amount) * currency, 2)
                    small_sum = round(int(i.price) * currency, 2)
                summary += local_sum
        try:
            context = {
                "items": cartItems,
                "amounts": b,
                "userId": str(request.user.id),
                "account": str(uid),
                "sum": summary,
                'currency': currency,
                'small_sum': small_sum,
            }
        except UnboundLocalError:
            context = {
            "items": cartItems,
            "amounts": b,
            "userId": str(request.user.id),
            "account": str(uid),
            "sum": summary,
            'currency': currency,
        }
        context.update(csrf(request))
        return render(request, template, context)


def userFavourites(request, uid):
    template = "accounts/profilePage/favourites.html"

    class ShopFavourite(models.Model):
        favourite_id = models.AutoField(primary_key=True)
        user_id = models.CharField(max_length=45)
        favourite_item = models.CharField(max_length=45, blank=True, null=True)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=45, blank=True, null=True)
        currency = models.CharField(max_length=45, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_favourite"

    if request.POST:
        itemToDelete = request.POST.get("delete", "")
        if itemToDelete:
            ShopFavourite.objects.filter(favourite_item=itemToDelete).delete()
        return redirect("/accounts/" + str(request.user.id) + "/favourites")
    else:
        favourites = ShopFavourite.objects.all()
        a = []
        for i in favourites:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
        context = {
            "favourites": a
            #'userId': str(request.user.id),
            #'account': str(uid),
        }
        context.update(csrf(request))
        return render(request, template, context)


def editProfilePage(request, uid):

    new_name = request.POST.get('new_name', '')
    new_last_name = request.POST.get('new_last_name', '')
    new_email = request.POST.get('new_email', '')
    new_phonenumber = request.POST.get('new_phonenumber', '')
    new_address = request.POST.get('new_address', '')
    password = request.POST.get('password', '')
    if request.POST:
        userProfile = AuthUser.objects.get(id=uid)
        userProfile.first_name = new_name
        userProfile.last_name = new_last_name
        userProfile.email = new_email
        userProfile.phone_number = new_phonenumber
        userProfile.address = new_address
        if check_password(password=password, encoded=userProfile.password) == True:
            userProfile.save()
            return redirect('/accounts/'+ str(uid))
        else:
            template = 'accounts/editProfile/edit.html'
            context = {
                'error_message': 'Неправильный пароль',
            }
            context.update(csrf(request))
            return render(request, template, context)  
    else:
        userProfile = AuthUser.objects.get(id=uid)
        template = 'accounts/editProfile/edit.html'
        context = {
            'userProfile': userProfile,
        }
        context.update(csrf(request))
        return render(request, template, context)

def editPasswordPage(request, uid):
    old_pwd = request.POST.get('old_pwd', '')
    new_pwd = request.POST.get('new_pwd', '')
    repeat_new_pwd = request.POST.get('repeat_new_pwd', '')
    userProfile = AuthUser.objects.get(id=request.user.id)
    template = 'accounts/editProfile/editPassword.html'
    if request.POST:
        if check_password(password=old_pwd , encoded=userProfile.password) == True:
            if new_pwd == repeat_new_pwd:
                username = userProfile.username
                hashed_pwd = make_password(repeat_new_pwd, salt=None, hasher='default')
                userProfile.password = hashed_pwd
                userProfile.save()
                user = auth.authenticate(username=username, password=repeat_new_pwd)
                auth.login(request, user)
                return redirect('/accounts/'+ str(uid))
            else:
                error_code = 'Новые пароли не совпадают. Повторите попытку'
                context = {
                'error_message': error_code,
            }
            return render(request, template, context)
        else:
            error_code = 'Неверный старый пароль. Попробуйте снова'
            context = {
                'error_message': error_code,
            }
            return render(request, template, context)
    else:
        template = 'accounts/editProfile/editPassword.html'
        return render(request, template)

def makeOrder(request, uid):

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
            db_table = "shop_cart"

    template = 'accounts/profilePage/makingOrder.html'
    user = AuthUser.objects.get(id=str(request.user.id))
    cart = ShopCarty.objects.all()
    a = []
    for i in cart:
        if str(i.user_id) == str(request.user.id):
            a.append(i.name)
    '''b = max(a)
    newUser = ShopCarty.objects.get(cart_id=b)'''
    context = {
        'user': user,
        'userCart': a,
    }
    return render(request, template, context)
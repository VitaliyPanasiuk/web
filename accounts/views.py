from django.http.response import HttpResponse
import bs4
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.template.context_processors import csrf
from .models import AuthUser, Продукт
from django.db import models
from django.db.models import F
from django.contrib import messages
import requests
from bs4 import BeautifulSoup as bs
import datetime
from django.contrib.auth.hashers import check_password, make_password

products = Продукт.objects.all()
accounts = AuthUser.objects.all()


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
    context = {
        "userId": str(request.user.id),
        "account": str(uid),
    }
    template = "accounts/profilePage/orders.html"
    return render(request, template, context)


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
url = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&ei=-JLVYJXzAcXUrgTlmouIAQ&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=Cgdnd3Mtd2l6EAMyCggAELEDEEYQggIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgUIABDJAzICCAA6BwgAEEcQsAM6BwgAELADEEM6BQgAELEDSgQIQRgAUKQkWM4uYPwwaAFwAngAgAHtAYgBrQeSAQUwLjYuMZgBAKABAaoBB2d3cy13aXrIAQrAAQE&sclient=gws-wiz&ved=0ahUKEwiVz8SOrrLxAhVFqosKHWXNAhEQ4dUDCA4&uact=5"


"""def parse(url):
    full_page = requests.get(url, headers=headers)
    soup = bs(full_page.content, "html.parser")
    convert = soup.findAll(
        "span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2}
    )
    return convert[0].text"""


usd_to_uah = ""
now = datetime.datetime.now()

"""if int(now.hour) == 11 and int(now.minute)==49: 
   print('gg')"""  # ?????????


def userCart(request, uid):
    # print(parse(url))
    template = "accounts/profilePage/cart.html"

    class ShopOrdery(models.Model):
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
    sum = 0
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
            b = 0
            userAccount = AuthUser.objects.get(id=request.user.id)
            userCarts = ShopCarty.objects.all()
            a = []
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
                order = ShopOrdery(имя=userAccount.first_name, фамилия=userAccount.last_name, почта=userAccount.email, дата_заказа=d, телефон=userAccount.phone_number, адрес_заказа=userAccount.address, сумма_заказа=sum, валюта_заказа='UAH', заказ=a, статус_оплаты='np', статус_заказа='nd')
                order.save()
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        i.delete()
                return redirect('/accounts/'+str(request.user.id))
    else:
        # print(parse(url))
        carts = ShopCarty.objects.all()
        cartItems = carts[0 : len(carts) :]
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
                    local_sum = int(i.price) * int(i.amount) * 27
                sum += local_sum
        context = {
            "items": cartItems,
            "amounts": b,
            "userId": str(request.user.id),
            "account": str(uid),
            "sum": str(sum),
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
from django.shortcuts import redirect, render
from django.contrib import auth
from django.template.context_processors import csrf
from .models import AuthUser, Продукт
from .forms import SignUpForm
from django.db import models
from django.db.models import F

products = Продукт.objects.all()
accounts = AuthUser.objects.all()
    
    

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/auth/register.html', {'form': form})



def login(request):
    args={}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Wrong username or password!'
            return render(request, 'accounts/auth/failed.html', args)
    
    else:
        return render(request, 'accounts/auth/login.html', args)
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def userProfilePage(request, uid):   
    context = {
        'userId': str(request.user.id),
        'account': str(uid),
    }
    template = 'accounts/profilePage/profilePage.html'
    return render(request, template, context)

def userOrders(request, uid):
    context = {
        'userId': str(request.user.id),
        'account': str(uid),
    }
    template = 'accounts/profilePage/orders.html'
    return render(request, template, context)

def userCart(request, uid):

    template = 'accounts/profilePage/cart.html'

    #ADD TO CART
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

    
    
    #DELETE FROM CART
    if request.POST:
        itemToDelete = request.POST.get('delete', '')
        addOneMore = request.POST.get('plus', '')
        removeOneMore = request.POST.get('minus', '')
        #carts = ShopCarty.objects.all()
        if addOneMore:
            item = request.POST.get('item_plus', '')
            carts = ShopCarty.objects.get(item=item)
            carts.amount += 1
            carts.save()                    
        elif removeOneMore:
            item = request.POST.get('item_minus', '')
            carts = ShopCarty.objects.get(item=item)
            carts.amount -= 1
            carts.save()
        elif itemToDelete:
            ShopCarty.objects.filter(item=itemToDelete).delete()
        return redirect('/accounts/' + str(request.user.id) + '/cart')
    else:
        carts = ShopCarty.objects.all()
        cartItems = carts[0:len(carts):]
        a = []
        b = []
        for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                a.append(cartItem.name)
                b.append(cartItem.amount)
        context = {
            'items': cartItems,
            'amounts': b,
            'userId': str(request.user.id),
            'account': str(uid),
        }
        context.update(csrf(request))
        return render(request, template, context)
    

def userFavourites(request, uid):
    context = {
        'userId': str(request.user.id),
        'account': str(uid),
    }
    template = 'accounts/profilePage/favourites.html'
    return render(request, template, context)
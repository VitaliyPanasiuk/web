from django.shortcuts import redirect, render
from django.contrib import auth
from django.template.context_processors import csrf
from .models import AuthUser, Продукт
from .forms import SignUpForm

accounts = AuthUser.objects.all()
products = Продукт.objects.all()

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
        'userId': request.user.id,
    }
    template = 'accounts/profilePage/profilePage.html'
    return render(request, template, context)

def userOrders(request, uid):
    context = {
        'userId': request.user.id,
    }
    template = 'accounts/profilePage/orders.html'
    return render(request, template, context)

def userCart(request, uid):
    productId = accounts[request.user.id-1].cart 
    context = {
        'item': products[int(productId)],
    }
    template = 'accounts/profilePage/cart.html'
    return render(request, template, context)

def userFavourites(request, uid):
    context = {
        'userId': request.user.id,
    }
    template = 'accounts/profilePage/favourites.html'
    return render(request, template, context)
from django.shortcuts import render, redirect
from .models import ShopProduct
from django.template.context_processors import csrf
from .models import AuthUser


продукты = ShopProduct.objects.all()

def addToCart(request, productId):
    context = {
        'выбранный_продукт': продукты[productId-1],
            }
    template = 'addToCart.html'
    context.update(csrf(request))
    if request.POST:
        addItemYes = request.POST.get('yes', '')
        if addItemYes:
            currentUser = AuthUser.objects.get(pk=request.user.id)
            itemsToSave = AuthUser(cart=addItemYes)
            currentUser.cart = str(addItemYes)
            currentUser.save()
            return redirect('/')
        else:
            return redirect('/products')
    
    else:
        return render(request, 'addToCart.html', context)

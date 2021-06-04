from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib import auth
from django.template.context_processors import csrf
from .models import AuthUser

from .forms import UserCreationForm


accounts = AuthUser.objects.all()

def register(request):
    args={}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username = newuser_form.cleaned_data['username'], password = newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render(request, 'accounts/auth/register.html', args)



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

from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.template.context_processors import csrf

'''class LoginFormView(FormView):
    form_class = AuthenticationForm
    success_url = '/products/34'
    template_name = 'accounts/login.html'
    
    def for_valid(self, form):
        form.save()
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return render(request, self.template_name)'''
'''
class RegisterFormView(TemplateView):
    form_class = UserCreationForm
    success_url = '/products/34'

    template_name = 'accounts/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
    
    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)'''

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
    return render(request, 'accounts/register.html', args)

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
            args['login_error'] = 'unknown user'
            return render(request, 'accounts/failed.html', args)
    
    else:
        return render(request, 'accounts/login.html', args)
    
def logout(request):
    auth.logout(request)
    return redirect('/')

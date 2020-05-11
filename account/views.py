from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
from account.forms import RegistrationForm, LoginForm

# ----------------------------------------------------------------------


def registo_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect('menu')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/registo.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('menu')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('perfil', user)
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('menu')


# ------------------------------------------------------------------------



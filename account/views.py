from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from account.forms import RegistrationForm, LoginForm, AccountUpdateForm
from account.models import Account


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
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('menu')
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('menu')


# ------------------------------------------------------------------------


def perfilutilizador(request, username):
    if not request.user.is_authenticated:
        return redirect('login_view')

    # account = get_object_or_404(Account, username=username)
    account = Account.objects.get(username=username)
    # account = request.user

    return render(request, 'account/perfil.html', {'account': account})


def account_settings(request, username):
    if not request.user.is_authenticated:
        return redirect('login_view')

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={"email": request.user.email,
                     "username": request.user.username,
                     "fotoPerfil": request.user.fotoPerfil,
                     }
        )

    context['account_form'] = form
    context['username'] = request.user.username
    return render(request, 'account/account.html', context)

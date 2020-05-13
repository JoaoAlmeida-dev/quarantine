from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Obrigatório, Adicione um email valido', widget=forms.EmailInput(attrs={'class': 'input'}))

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
        }


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = Account
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'password': forms.PasswordInput(attrs={'class': 'input'}),
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Login Invalido')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'fotoPerfil')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input'}),
            'fotoPerfil': forms.TextInput(attrs={'class': 'input'}),
        }

        def clean_email(self):
            if self.is_valid():
                email = self.clean_email['email']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                except Account.DoesNotExist:
                    return email
                raise forms.ValidationError('Email "%s" já está registado.' % account)

        def clean_username(self):
            if self.is_valid():
                username = self.cleaned_data['username']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                except Account.DoesNotExist:
                    return username
                raise forms.ValidationError('Username "%s" já está a ser utilizado.' % username)

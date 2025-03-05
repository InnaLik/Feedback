from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import User


# этот класс по сути нужен, чтобы применять валидаторы на вводимые данные
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Введите ваше имя пользователя",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Введите ваш пароль",
            }
        ),
    )

    class Meta:
        # с какой моделью будем работать
        model = User
        fields = ['username', 'password']

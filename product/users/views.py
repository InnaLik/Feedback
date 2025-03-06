from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # проверка, есть ли такой пользователь
            user = auth.authenticate(username=username, password=password)
            if user:
                # логиним пользователя
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    # если у нас пришел post запрос, но не валидный, в контекст передастся форма не пустая, так как выше мы её сделали
    # на сайте останется логин, пароль сбросится
    context = {'title': 'Авторизация', 'form': form}

    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # заносим данные в бд
            form.save()
            # сразу войдем под пользователем
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {'title': 'Регистрация', 'form': form}

    return render(request, 'users/registration.html', context)


def profile(request):
    context = {'title': 'Кабинет'}

    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

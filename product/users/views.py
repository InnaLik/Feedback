from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


# Create your views here.
def login(request):
    """Вход в уз."""
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
                messages.success(request, message=f"{username}, Вы успешно зарегистрировались")
                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    # если у нас пришел post запрос, но не валидный, в контекст передастся форма не пустая, так как выше мы её сделали
    # на сайте останется логин, пароль сбросится
    context = {'title': 'Авторизация', 'form': form}

    return render(request, 'users/login.html', context)


def registration(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # заносим данные в бд
            form.save()
            # сразу войдем под пользователем
            user = form.instance
            auth.login(request, user)
            messages.success(request, message=f"{user.username}, Вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {'title': 'Регистрация', 'form': form}

    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    """Профиль пользователя."""
    if request.method == 'POST':
        # files чтобы могла принимать файлы
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            # заносим данные в бд
            form.save()
            messages.success(request, message="Данные изменены")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        # передаем объект самого пользователя
        form = ProfileForm(instance=request.user)
    context = {'title': 'Кабинет', 'form': form}

    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    """Выход из уз."""
    messages.success(request, message=f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))


def users_cart(request):
    return render(request, 'users/users_cart.html')

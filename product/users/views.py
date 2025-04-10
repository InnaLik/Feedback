from carts.models import Cart
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.utils import update_carts


class UserLoginView(LoginView):
    """Класс представления для авторизации пользователей."""

    template_name = 'users/login.html'
    # наша форма
    form_class = UserLoginForm
    # куда перенаправлять, если вход успешен
    # success_url = reverse_lazy('main:index')

    def get_success_url(self):
        """
        Если в POST запросе есть next, то перенаправляем пользователя туда, откуда он пришел после регистрации,
        при условии, что это не logout, иначе перенаправляем пользователя на главную страницу.
        """
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context

    def form_valid(self, form):
        """Чтобы после авторизации корзина пользователя не пропала."""
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, message=f"{user.username}, Вы успешно зарегистрировались")
            return HttpResponseRedirect(self.get_success_url())


# тут посмотреть, потому что если один и тот же товар добавили под незарег пользователем и зарег,
# то у него будут разные id
def registration(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # заносим данные в бд
            form.save()

            session_key = request.session.session_key

            # сразу войдем под пользователем
            user = form.instance
            auth.login(request, user)
            messages.success(request, message=f"{user.username}, Вы успешно зарегистрировались")

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                update_carts(user)

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
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(Prefetch("orderitem_set", queryset=OrderItem.object.select_related("product")))
        .order_by("-id")
    )
    context = {'title': 'Кабинет', 'form': form, "orders": orders}

    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    """Выход из уз."""
    messages.success(request, message=f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))


def users_cart(request):
    """Для отображения корзины пользователя."""
    return render(request, 'users/users_cart.html')

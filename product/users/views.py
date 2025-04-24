from carts.models import Cart
from common.mixins import CacheMixin
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


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


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    # наша форма
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    # запускается в том случае, если пользователь прошел валидацию
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, message=f"{user.username}, Вы успешно зарегистрировались")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context


# миксин вместо декоратора
class ProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    """Профиль пользователя."""

    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        from orders.models import Order, OrderItem

        context = super().get_context_data(**kwargs)
        context['title'] = "Кабинет"
        query = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(Prefetch("orderitem_set", queryset=OrderItem.object.select_related("product")))
            .order_by("-id")
        )
        # получаем значения из кэша
        orders = self.set_get_cache(query, f"orders_for_user_{self.request.user.id}", 60)
        context['orders'] = orders
        return context

    def get_object(self, queryset=None):
        """Для возврата пользователя сразу из запроса, а не из бд."""
        return self.request.user

    def form_valid(self, form):
        """Для отправки пользователю сообщения об успешном изменении данных."""
        messages.success(self.request, message="Данные изменены")
        return super().form_valid(form)


# @login_required
# def logout(request):
#     """Выход из уз."""
#     messages.success(request, message=f"{request.user.username}, Вы вышли из аккаунта")
#     auth.logout(request)
#     return redirect(reverse('main:index'))


class UserCartView(TemplateView):
    """Для отображения корзины пользователя."""

    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Корзина"
        return context

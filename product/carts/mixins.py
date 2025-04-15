from carts.models import Cart
from carts.utils import get_user_carts
from django.template.loader import render_to_string
from django.urls import reverse


class CartMixin:
    @staticmethod
    def get_cart(request, product=None, cart_id=None):
        """Получение корзины пользователя."""
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product

        if cart_id:
            query_kwargs["id"] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    @staticmethod
    def render_cart(request):
        """Для создания HTML-фрагмента корзины, адаптированного под текущую ситуацию."""
        # получаю корзину пользователя
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}
        #  Получаем URL страницы, с которой пришёл запрос.
        referer = request.META.get("HTTP_REFERER")
        # Проверка: если пользователь пришёл со страницы создания заказа
        if reverse("orders:create_order") in referer:
            context["order"] = True

        return render_to_string("carts/includes/included_cart.html", context, request=request)

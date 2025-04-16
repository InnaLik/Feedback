from carts.models import Cart
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy("user:profile")

    def get_initial(self):
        """Предзаполнение полей."""
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            # атомарная транзакция, все ниже происходит в рамках одной транзакции,
            # коммит создается только, если нет ошибок
            with transaction.atomic():
                # пользователь
                user = self.request.user
                # сохраняем все корзины пользователя
                cart_items = Cart.objects.filter(user=user)
                # если корзины имеются
                if cart_items.exists():
                    # Создаем заказ по форме
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.price
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValueError(
                                f'Недостаточное количество товара на складе {name} в наличии {product.quantity}'
                            )
                        # записываем в бд информацию по проданным товарам
                        OrderItem.object.create(order=order, product=product, name=name, price=price, quantity=quantity)
                        product.quantity -= quantity
                        product.save()
                    # удаляем эти товары из корзин пользователя, так как заказ оформлен и
                    # далее работаем уже с другой табличкой в бд
                    # чтобы не было такого, что пользователь заказал корзину, заходит в корзину,
                    # а там снова эти товары тусуются
                    cart_items.delete()

                    messages.success(self.request, message="Заказ оформлен")
                    # возвращаем пользователя на его профиль
                    return redirect('user:profile')
        except ValidationError as e:
            messages.success(self.request, str(e))
            # если ошибка валидации, то заново пользователю отображаем страницу с корзиной
            return redirect('cart:order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Заказ не оформлен")
        return redirect('orders:create_order')

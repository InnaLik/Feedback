from carts.models import Cart
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, render
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


def create_order(request):
    """Создание заказа."""
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # пользователь
                    user = request.user
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
                            name = cart_item.name
                            price = cart_item.price
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValueError(
                                    f'Недостаточное количество товара на складе {name} в наличии {product.quantity}'
                                )
                            # записываем в бд информацию по проданным товарам
                            OrderItem.object.create(
                                order=order, product=product, name=name, price=price, quantity=quantity
                            )
                            product.quantity -= quantity
                            product.save()
                        # удаляем эти товары из корзин пользователя, так как заказ оформлен и
                        # далее работаем уже с другой табличкой в бд
                        # чтобы не было такого, что пользователь заказал корзину, заходит в корзину,
                        # а там снова эти товары тусуются
                        cart_items.delete()

                        messages.success(request, message="Заказ оформлен")
                        # возвращаем пользователя на его профиль
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                # если ошибка валидации, то заново пользователю отображаем страницу с корзиной
                return redirect('cart:order')

    else:

        initial = {'first_name': request.user.first_name, 'last_name': request.user.last_name}
        # создаем пустую форму, если пользователь только зашел в оформление заказа
        form = CreateOrderForm(initial=initial)

    context = {"title": 'Оформление заказа', "form": form}

    return render(request, 'orders/create_order.html', context)

# from django.shortcuts import render
from carts.models import Cart
from django.contrib import messages
from django.shortcuts import redirect
from goods.models import Products


def cart_add(request, product_slug):
    """Добавляет товар в корзину."""
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        # если у пользователя уже есть товар в корзине
        if carts.exists():
            # берем просто элемент, там же пришел queryset, а нам нужен объект, для этого берем первый или не важно
            # какой все равно там будет одна запись в таблице
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    messages.success(request, message="Товар успешно добавлен в корзину")
    # возвращаем пользователя на ту же страницу, где он был
    return redirect(request.META['HTTP_REFERER'])


def cart_change(request, product_slug):
    """Меняет количество товара в корзине."""


def cart_remove(request, product_slug):
    """Удаляет товар из корзины."""
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, product=product).first()
        if cart:
            cart.delete()

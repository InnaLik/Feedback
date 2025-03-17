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


def cart_change(request, cart_id, sing):
    """Меняет количество товара в корзине."""
    pass


def cart_remove(request, cart_id):
    """Удаляет товар из корзины."""
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=cart_id)
        if cart:
            name_product = cart.product.name
            cart.delete()
            messages.success(request, f"{name_product} был удален")
        else:
            messages.success(request, "Товар либо уже был удален из корзины, либо не был добавлен")

    return redirect(request.META['HTTP_REFERER'])

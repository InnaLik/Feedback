from carts.models import Cart
from carts.utils import get_user_carts
from django.http import JsonResponse
from django.template.loader import render_to_string
from goods.models import Products


def cart_add(request):
    """Добавляет товар в корзину."""
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)
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
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {"message": "Товар добавлен в корзину", "cart_items_html": cart_items_html}

    return JsonResponse(response_data)


def cart_change(request, cart_id, sing):
    """Меняет количество товара в корзине."""
    pass


def cart_remove(request):
    """Удаляет товар из корзины."""
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string("carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {"message": "Товар удален", "cart_items_html": cart_items_html, "quantity_deleted": quantity}

    return JsonResponse(response_data)

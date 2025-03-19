from carts.models import Cart


def get_user_carts(request):
    """Получение корзин пользователя."""
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        return carts

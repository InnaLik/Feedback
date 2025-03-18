from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        return carts

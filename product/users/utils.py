from carts.models import Cart


def update_carts(user):
    Cart.objects.filter(user=user).merge_duplicates()

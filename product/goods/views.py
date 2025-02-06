from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, category_slug):
    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    else:
        # get_list_or_404 нужно для того, чтобы при возвращении пустого queryset выводилась 404 ошибка
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    # по три товара на каждую страницу
    paginator = Paginator(goods, per_page=3)
    # текущая страница, это и будет на queryset урезанный до 3х
    current_page = paginator.page(1)

    context = {"title": "Мой каталог",
               'goods': current_page}

    return render(request, 'goods/catalog.html', context=context)

def get_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {"product": product}

    return render(request, 'goods/product.html', context=context)



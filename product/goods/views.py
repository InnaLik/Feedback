from django.shortcuts import render

from goods.models import Products


def catalog(request, category_slug):
    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    context = {"title": "Мой каталог",
               'goods': goods}

    return render(request, 'goods/catalog.html', context=context)

def get_product(request, slug_url):
    product = Products.objects.get(slug=slug_url)
    context = {"product": product}

    return render(request, 'goods/product.html', context=context)



from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.views.generic import DetailView
from goods.models import Products
from goods.utils import q_search


def catalog(request, category_slug=None):
    # получаем параметр страницы через GET запрос
    page = request.GET.get("page", 1)
    query = request.GET.get("q", None)
    on_rating = request.GET.get("on_rating", None)
    order_by = request.GET.get("order_by", None)
    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        # get_list_or_404 нужно для того, чтобы при возвращении пустого queryset выводилась 404 ошибка
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_rating:
        goods = goods.order_by("-rating")

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    # по три товара на каждую страницу
    paginator = Paginator(goods, per_page=6)
    # текущая страница, это и будет на queryset урезанный до 6
    current_page = paginator.page(int(page))

    context = {"title": "Мой каталог", 'goods': current_page, "slug_url": category_slug}

    return render(request, 'goods/catalog.html', context=context)


class ProductView(DetailView):
    """Класс для представления информации об одной единицы товара."""

    template_name = 'goods/product.html'
    slug_url_kwarg = "product_slug"
    # это то имя, под которым мы потом будем обращаться в нашем шаблоне к параметрам
    context_object_name = "product"

    # переопределение
    def get_object(self, queryset=None):
        """Получение объекта для отображения."""
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

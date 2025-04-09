from django.views.generic import DetailView, ListView
from goods.models import Products
from goods.utils import q_search


class CatalogView(ListView):
    # Авто-подгрузка данных из модели
    model = Products
    # queryset = Products.objects.all().order_by("-rating")
    template_name = 'goods/catalog.html'
    # количество товаров, которое будет отображаться на странице
    paginate_by = 6
    # Удобное имя списка объектов в шаблоне
    context_object_name = "goods"
    # если не будет товаров, то автоматически будет ошибка 404
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        query = self.request.GET.get("q")
        on_rating = self.request.GET.get("on_rating")
        order_by = self.request.GET.get("order_by")

        if category_slug == "vse-tovary":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)

        if on_rating:
            goods = goods.order_by("-rating")

        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мой каталог"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context


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

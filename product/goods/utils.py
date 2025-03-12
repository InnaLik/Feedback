from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models.manager import BaseManager
from goods.models import Products


def q_search(query) -> BaseManager[Products]:
    """
    Возвращает queryset товаров, которые пользователь ввел в строку поиска. Поиск производится по id или
    имени и названию.

    Args:
        query: Строка из строки поиска.

    Return:
        Queryset товаров.
    """
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    # запросы будут отсортированы по релевантности, то есть от более похожих к менее похожим
    # rank__gt=0 - чтобы не все данные выходили, а там где совпадение больше нуля
    vector = SearchVector("name", "description")
    query = SearchQuery(query)
    products = Products.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
    # чтобы выделялись строчки, по которым происходит поиск
    products = products.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )
    products = products.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )
    return products

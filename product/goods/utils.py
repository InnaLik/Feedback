from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.db.models import Q
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
    vector = SearchVector("name", "description")
    return Products.objects.annotate(rank=SearchRank(vector, SearchQuery(query))).order_by("-rank")

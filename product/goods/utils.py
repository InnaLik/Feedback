from django.db.models.manager import BaseManager

from goods.models import Products
from django.db.models import Q


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
    keywords = [word for word in query.split() if len(word) > 2]
    q_objects = Q()

    for token in keywords:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(name__icontains=token)

    return Products.objects.filter(q_objects)
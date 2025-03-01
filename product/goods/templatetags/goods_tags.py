from urllib.parse import urlencode

from django import template
from django.utils.http import urlencode  # noqa

from goods.models import Categories

# для регистрации тега создаем регистер
register = template.Library()


@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


@register.filter
def stars(value):
    full_star = '★'
    empty_star = '☆'
    return f'{full_star * value}{empty_star * (10 - value)}'


# takes_context=True все контекстные переменные будут доступны через context
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    # формируем словарь с данными
    query = context['request'].GET.dict()
    # расширяем словарь нашим и значениями в случае с пагинацией это page
    query.update(kwargs)
    # urlencode уже формирует параметры в виде строки, которые можно использовать в url адресе
    return urlencode(query)

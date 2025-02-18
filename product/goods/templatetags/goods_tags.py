from goods.models import Categories
from django import template

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
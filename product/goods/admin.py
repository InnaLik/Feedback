from django.contrib import admin
from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # для автоматического заполнения полей
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        'name',
    ]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # для автоматического заполнения полей
    prepopulated_fields = {"slug": ("name",)}
    # поля, которые отображаются в админ панели
    list_display = ['name', 'price', 'rating', 'category']
    # поля, которые можно изменять
    list_editable = ['price', 'rating']
    # поля, по которым можно искать
    search_fields = ['name', 'description']
    # поля, по которым можно фильтровать
    list_filter = ['rating', 'category']
    # какие элементы нужны для отображения в карточке
    fields = ['name', 'slug', 'description', 'image', 'price', 'rating', 'category' 'quantity']

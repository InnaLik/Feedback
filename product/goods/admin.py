# Register your models here.

from django.contrib import admin

from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    # для автоматического заполнения полей
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # для автоматического заполнения полей
    prepopulated_fields = {"slug": ("name", )}
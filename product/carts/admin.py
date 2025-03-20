from carts.models import Cart
from django.contrib import admin


class CartTabAdmin(admin.TabularInline):
    """Класс для отображения его в других моделях в админ панели."""

    model = Cart
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ("created_timestamp",)
    # свободное поле для добавления пользователю новых заказов
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_timestamp']
    list_filter = ['created_timestamp', 'user', 'product__name']

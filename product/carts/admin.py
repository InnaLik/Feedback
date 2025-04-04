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
    list_display = ['user_display', 'product', 'quantity', 'created_timestamp']
    list_filter = ['created_timestamp', 'user', 'product__name']

    @staticmethod
    def user_display(obj):
        """
        Для отображения имени пользователя в админ панели.

        Returns:
            str метод объекта obj.user или строка "Анонимный пользователь".
        """
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)

    # user_display and product_display alter name of columns in admin panel
    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"

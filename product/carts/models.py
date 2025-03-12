from django.db import models
from goods.models import Products

from product import settings


# класс queryset для корзины
class CartQueryset(models.QuerySet):

    def total_price(self):
        """Общая сумма товаров в корзине."""
        return sum(cart.get_product_price() for cart in self)

    def total_quantity(self):
        """Общее количество товаров в корзине."""
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь'
    )
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    # расширяем, чтобы помимо стандартных методов (filter, ...) были доступны методы из CartQueryset
    objects = CartQueryset().as_manager()

    def get_product_price(self):
        """Итоговая стоимость. Например, 2 крема * 2 штуки."""
        return self.product.price * self.quantity

    def __str__(self):
        return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'

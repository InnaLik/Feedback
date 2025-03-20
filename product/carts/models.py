from django.db import models
from django.db.models import Sum
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

    def merge_duplicates(self):
        """Объединяет дублирующиеся товары в корзине, суммируя их количество."""
        carts = self.values("product").annotate(total_quantity=Sum("quantity"))

        for cart in carts:
            product_id = cart["product"]
            total_quantity = cart["total_quantity"]

            # Оставляем одну запись и обновляем её количество
            main_cart = self.filter(product_id=product_id).first()
            main_cart.quantity = total_quantity
            main_cart.save()

            # Удаляем все дубликаты, кроме оставленной записи
            self.filter(product_id=product_id).exclude(id=main_cart.id).delete()


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
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'

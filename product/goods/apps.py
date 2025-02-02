from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods'
    # для админ панели для отображения корректного названия
    verbose_name = 'Товары'

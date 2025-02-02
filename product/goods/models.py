from django.db import models


class Categories(models.Model):
    # здесь verbose_name для админ панели
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименование категории')
    slag = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')

    class Meta:
        # как будет называться таблица в бд
        db_table = 'category'
        # как будет отображаться в админ панели
        verbose_name = 'Категория'
        # как будет отображаться в админ панели при множественном числе
        verbose_name_plural = 'Категории'

from django.db import models


class Categories(models.Model):
    # здесь verbose_name для админ панели
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        # как будет называться таблица в бд
        db_table = 'category'
        # как будет отображаться в админ панели
        verbose_name = 'Категорию'
        # как будет отображаться в админ панели при множественном числеx
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

def get_default_category_id():
    return Categories.objects.get_or_create(name="Без категории")[0].id

class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименование продукта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True,verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(to=Categories, on_delete=models.SET_DEFAULT, default=get_default_category_id, verbose_name='Категория')


    class Meta:
        # как будет называться таблица в бд
        db_table = 'product'
        # как будет отображаться в админ панели
        verbose_name = 'Продукт'
        # как будет отображаться в админ панели при множественном числе
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
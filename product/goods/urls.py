from django.urls import path

from goods.views import catalog, product

# чтобы работал namespace
app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='index'),
    path('product/', product, name='product'),
]
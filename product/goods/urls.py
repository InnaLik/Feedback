from django.urls import path

from goods.views import catalog, get_product

# чтобы работал namespace
app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='index'),
    path('product/<int:product_id>/', get_product, name='get_product'),
]
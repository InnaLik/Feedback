from django.urls import path

from goods.views import catalog, get_product

# чтобы работал namespace
app_name = 'catalog'

urlpatterns = [
    path('<slug:category_slug>/', catalog, name='index'),
    path('product/<slug:product_slug>/', get_product, name='get_product'),
]
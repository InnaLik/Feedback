from django.urls import path
from goods.views import ProductView, catalog

# чтобы работал namespace
app_name = 'catalog'

urlpatterns = [
    path('search/', catalog, name='search'),
    path('<slug:category_slug>/', catalog, name='index'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='get_product'),
]

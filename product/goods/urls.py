from django.urls import path
from goods.views import CatalogView, ProductView

# чтобы работал namespace
app_name = 'catalog'

urlpatterns = [
    path('search/', CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='get_product'),
]

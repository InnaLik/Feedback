from django.urls import path
from orders import views

# чтобы работал namespace
app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
]

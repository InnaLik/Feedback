from django.urls import path

from users import views

# чтобы работал namespace
app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='reqistration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]

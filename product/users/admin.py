from carts.admin import CartTabAdmin
from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # поля, которые отображаются в админ панели
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    # для отображения корзин пользователя
    inlines = [
        CartTabAdmin,
    ]

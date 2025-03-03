from django.contrib.auth.forms import AuthenticationForm
from users.models import User


# этот класс по сути нужен, чтобы применять валидаторы на вводимые данные
class UserLoginForm(AuthenticationForm):

    class Meta:
        # с какой моделью будем работать
        model = User

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUsers:
    @pytest.mark.parametrize(
        "path_name, template, title",
        [
            ("user:login", "users/login.html", "Авторизация"),
            ("user:registration", "users/registration.html", "Регистрация"),
            # ("user:profile", "users/profile.html", "Кабинет"),
        ],
    )
    def test_success_pages(self, client, path_name, template, title):
        path = reverse(path_name)
        response = client.get(path)
        assert response.status_code == 200
        assert response.templates[0].name == template
        assert response.context['title'] == title

        assert title in response.content.decode()

    @pytest.mark.django_db
    def test_logout_success(self, client, django_user_model):
        user = django_user_model.objects.create_user( # noqa
            username="testuser", password="password"
        )
        client.login(username="testuser", password="password")  # Логиним пользователя

        response = client.post(reverse("user:logout"))  # Выходим

        assert response.status_code == 302  # Проверяем редирект
        assert not client.session.get("_auth_user_id")

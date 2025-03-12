import pytest
from django.urls import reverse
from users.forms import ProfileForm


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
        user = django_user_model.objects.create_user(username="testuser", password="password")  # noqa
        client.login(username="testuser", password="password")  # Логиним пользователя

        response = client.post(reverse("user:logout"))  # Выходим

        assert response.status_code == 302  # Проверяем редирект
        assert not client.session.get("_auth_user_id")

    @pytest.mark.django_db
    def test_logout_without_auth(self, client):
        response = client.post(reverse("user:logout"))  # Выход без входа в систему

        assert response.status_code == 302  # Проверяем, что всё равно происходит редирект
        assert response.url.startswith(reverse("user:login"))

    @pytest.mark.django_db
    def test_profile_get(self, client, django_user_model):
        user = django_user_model.objects.create_user(username="testuser", password="password")  # noqa  # noqa
        client.login(username="testuser", password="password")  # Логиним пользователя

        response = client.get(reverse("user:profile"))  # Открываем страницу профиля

        assert response.status_code == 200  # Проверяем успешный ответ
        assert "Кабинет" in response.content.decode()  # Проверяем заголовок страницы
        assert isinstance(response.context["form"], ProfileForm)  # Проверяем, что передана форма

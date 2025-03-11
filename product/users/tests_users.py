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

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestMain:

    @pytest.mark.parametrize(
        "path_name, template, title, content",
        [
            ("main:index", "main/index.html", "Home - Главная", "Отзывы о продуктах"),
            ("main:about", "main/about.html", "Home - обо мне", "Обо мне"),
        ],
    )
    def test_success_pages(self, client, path_name, template, title, content):
        path = reverse(path_name)
        response = client.get(path)
        assert response.status_code == 200
        assert response.templates[0].name == template
        assert response.context['title'] == title
        assert response.context['content'] == content

        assert title in response.content.decode()
        assert content in response.content.decode()

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestMain:

    def test_success_main_page(self, client):
        path = reverse('main:index')
        response = client.get(path)
        assert response.status_code == 200
        assert response.templates[0].name == 'main/index.html'
        assert response.context['title'] == "Home - Главная"
        assert response.context['content'] == "Отзывы о продуктах"

        assert "Home - Главная" in response.content.decode()
        assert "Отзывы о продуктах" in response.content.decode()

    def test_success_about(self, client):
        path = reverse('main:about')
        response = client.get(path)
        assert response.status_code == 200
        assert response.templates[0].name == 'main/about.html'
        assert response.context['title'] == 'Home - обо мне'
        assert response.context['content'] == 'Обо мне'
        assert response.context['text_on_page'] == 'Программист мечтатель'

        assert "Home - обо мне" in response.content.decode()
        assert "Обо мне" in response.content.decode()
        assert "Программист мечтатель" in response.content.decode()

from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Класс представления главной страницы."""

    template_name = 'main/index.html'

    # переопределение
    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - Главная"
        context['content'] = "Отзывы о косметике"
        return context


class AboutView(TemplateView):
    """Класс представления страницы О нас."""

    template_name = 'main/about.html'
    # если нам не нужны параметры get запроса/ переопределение
    extra_context = {"title": "Home - обо мне", "content": "Обо мне", "text_on_page": "Программист мечтатель"}


class PageNotFoundView(View):
    """Класс для обработки 404 ответа."""

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound(
            "<h1>Страница не найдена или удалена, или её не добавили. Обратитесь к разработчику</h1>"
        )

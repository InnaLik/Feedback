from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Класс представления главной страницы."""

    template_name = 'main/index.html'

    # переопределение
    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - Главная"
        context['content'] = "Отзывы о продуктах"
        return context


class AboutView(TemplateView):
    """Класс представления страницы О нас."""

    template_name = 'main/about.html'
    # если нам не нужны параметры get запроса/ переопределение
    extra_context = {"title": "Home - обо мне", "content": "Обо мне", "text_on_page": "Программист мечтатель"}

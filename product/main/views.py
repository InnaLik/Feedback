from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Класс представления главной страницы."""

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - Главная"
        context['content'] = "Отзывы о продуктах"
        return context


class AboutView(TemplateView):
    """Класс представления страницы О нас."""

    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        """Для добавления контекста."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - обо мне"
        context['content'] = "Обо мне"
        context['text_on_page'] = "Программист мечтатель"
        return context

from django.shortcuts import render

from goods.models import Categories


# Create your views here.
def index(request):
    categories = Categories.objects.all()

    context = {"title": "Home - Главная",
               "content": "Отзывы о продуктах",
               "categories": categories}
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {"title": "Home - обо мне",
               "content": "Обо мне",
               "text_on_page": "Программист мечтатель"}
    return render(request, 'main/about.html', context=context)
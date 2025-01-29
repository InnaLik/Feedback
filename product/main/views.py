from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"title": "Home - Главная",
               "content": "Отзывы о продуктах"}
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {"title": "Home - обо мне",
               "content": "Обо мне",
               "text_on_page": "Программист мечтатель"}
    return render(request, 'main/about.html', context=context)
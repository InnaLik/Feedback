from lib2to3.fixes.fix_input import context

from django.shortcuts import render

# Create your views here.

def catalog(request):
    # для примера и обучения
    context = {"title": "Мой каталог",
               'goods': [{'image': 'deps/images/products/6679488559.jpg',
                         'name': 'Палетка теней MaxFactor',
                         'feed_desc': 'Быстро скатываются и осыпаются, уже через час',
                         'price': 300.00},
                        {
                            'image': 'deps/images/products/arko.jpg',
                            'name': 'Крем для рук Arko',
                            'feed_desc': 'Очень жирный, кожу не увлажняет',
                            'price': 70.00
                         },
                        {
                            'image': 'deps/images/products/revolution.png',
                            'name': 'Тени revolution',
                            'feed_desc': 'Не скатываются, долго держатся, но не подошел цвет',
                            'price': 1000.00
                        },
                        {
                            'image': 'deps/images/products/крем для лица darling_.png',
                            'name': 'Крем для лица Darling',
                            'feed_desc': 'хороший легкий крем, но недостаточно для увлажнения, не выравнивает кожу, '
                                         'общая оценка 5 из 10, за легкость структуры и пористость. Его лучше не покупать.',
                            'price': 2000.00
                        },
                        {
                            'image': 'deps/images/products/помада.png',
                            'name': 'Помада Vivien sabo',
                            'feed_desc': 'Не держится, маркая',
                            'price': 300.00
                        },
                        {
                            'image': 'deps/images/products/тушь дарлинг.png',
                            'name': 'Тушь Darling силикон',
                            'feed_desc': 'Отличная тушь, хорошо смывается, покупаем.',
                            'price': 500
                        },
                        {
                            'image': 'deps/images/products/тушь vivienne.png',
                            'name': 'Viviene Sabo белая/черная ',
                            'feed_desc': 'Быстро осыпается, тяжело смыть',
                            'price': 500
                        }]}

    return render(request, 'goods/catalog.html', context=context)

def product(request):
    return render(request, 'goods/product.html')
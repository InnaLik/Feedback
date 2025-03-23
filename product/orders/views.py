from django.shortcuts import render


def create_order(requests):
    return render(requests, 'orders/create_order.html')

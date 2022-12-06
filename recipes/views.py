from django.http import HttpResponse
from django.shortcuts import render

# HTTP request <- HTTP response
# Cliente pede <- Server responde/devolve


def home(request):
    return render(request, 'recipes/home.html', context={
        'name': 'Lucas'
    })


def sobre(request):
    return render(request, 'recipes/sobre.html')


def contato(request):
    return HttpResponse('CONTATO')

# from django.http import Http404 - igual ao que está embaixo, if1
# from django.http import HttpResponse - Para o if2 com comentário.
# Serve para mostrar página que não existe.

import os

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Recipe

# HTTP request <- HTTP response
# Cliente pede <- Server responde/devolve


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE
    )

    messages.error(request, 'Que legal sua mensagem foi um sucesso!')
    messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    messages.info(request, 'Epa, você foi pesquisar algo que eu vi.')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE
    )

    # 1 if not recipes:
    # 1    raise Http404('Not Found')

    # 2 if not recipes:
    # 2    return HttpResponse(content='Not Found', status=404)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj, 'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE
    )

    return render(request, 'recipes/pages/search.html',
                  {'page_title': f'Search for "{search_term}" |',
                   'search_term': search_term,
                   'recipes': page_obj, 'pagination_range': pagination_range,
                   'additional_url_query': f'&q={search_term}',
                   })

from django.urls import path

from . import views

# Por urls ser irmão de views é possível trocar o nome do 'pai' recipes
# por um .(ponto)

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/category/<int:category_id>/',
         views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/search/', lambda request: ..., name="search"),
]

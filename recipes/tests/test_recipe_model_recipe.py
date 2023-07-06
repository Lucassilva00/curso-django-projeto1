from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipes_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='categoria teste'),
            author=self.make_author(username='newusertest'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slugs',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            serving_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    # self.recipe.save()  # O django salva na base de dados
    # self.fail(self.recipe.title) Falha o código de propósito

    # parametriza um teste, o .expand é usado por ter uma lista

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('serving_unit', 65),
    ])
    def test_recipe_field_max_length(self, field, max_length):
        # for field, max_length in fields:
        # Este self.subTest como diz o nome cria subtestes, e só é possível
        # ver a falha de cada subteste pelo python manage.py test,
        # portanto no pytest não funciona
        # with self.subTest(field=field, max_length=max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        # Avisa que vai levantar um erro de validação(ValidationError),
        # caso contrário trava o código
        with self.assertRaises(ValidationError):
            # Executa validação e não trava o teste se não passar na validação
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        # need recipe
        recipe = self.make_recipes_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparation_steps_is_html is not False')

    def test_recipe_is_published_is_false_by_default(self):
        # need recipe
        recipe = self.make_recipes_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not False')

    def test_recipe_string_representation(self):
        needed = 'Title representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
                         msg=f'Recipe string representation must be {needed} but {self.recipe.title} was received.')

from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

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

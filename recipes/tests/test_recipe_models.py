from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'a'*70
        # Avisa que vai levantar um erro de validação(ValidationError),
        # caso contrário trava o código
        with self.assertRaises(ValidationError):
            # Executa validação e não trava o teste se não passar na validação
            self.recipe.full_clean()

        # self.recipe.save()  # O django salva na base de dados
        # self.fail(self.recipe.title) Falha o código de propósito

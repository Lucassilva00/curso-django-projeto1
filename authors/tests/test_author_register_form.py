from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your Username'),
        ('email', 'Your Email'),
        ('first_name', 'Type your first name...'),
        ('last_name', 'Type your last name...'),
        ('password', 'Type your password...'),
        ('password2', 'Repeat your password...'),
    ])
    def test_fields_placeholder_is_correct(self, field, placehold):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, placehold)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),  # noqa E501
        ('email', 'The email must be valid'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        help_text = form[field].field.help_text

        self.assertEqual(needed, help_text)

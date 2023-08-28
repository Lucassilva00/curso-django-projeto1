from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'Email'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label_is_correct(self, field, needed):
        form = RegisterForm()
        label = form[field].field.label

        self.assertEqual(label, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'str0ngP@ssword1',
            'password2': 'str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'Type your email'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

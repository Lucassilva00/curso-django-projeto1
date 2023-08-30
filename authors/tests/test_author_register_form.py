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
        ('username', 'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'),  # noqa E501
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
            'password': '1',
            'password2': '1',
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

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A'*151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have 150 characters or less'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = ('Password must have at least one uppercase letter, '
               'one lowercase letter and one number. The length should be '
               'at least 8 characters.')

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'A@abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'A@abc123'
        self.form_data['password2'] = 'A@abc123A'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = ('Password and password2 must be equal.')

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'A@abc123'
        self.form_data['password2'] = 'A@abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        errors = response.context['form'].errors.get('email')
        if errors is not None:
            self.assertIn(msg, errors)
        errors2 = response.content.decode('utf-8')
        if errors is not None:
            self.assertIn(msg, errors2)

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'Abc123456',
            'password2': 'Abc123456'
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='Abc123456'
        )

        self.assertTrue(is_authenticated)

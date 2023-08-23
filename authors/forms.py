from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your Username')
        add_placeholder(self.fields['email'], 'Your Email')
        add_placeholder(self.fields['first_name'],
                        'Type your first name...')
        add_placeholder(self.fields['last_name'],
                        'Type your last name...')

    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repeat your password here...'  # noqa E501
                                }))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # semelhante a criação pelo método acima de escolher os campos, com exclude todos campos são selecionados menos aqueles presentes no exclude # noqa E501
        # exclude = ['first_name']

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }

        # Altera os help texts
        help_texts = {
            'email': 'The email must be valid',
            'password': 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'

        }

        # Altera as mensagens de erro
        error_messages = {
            'username': {
                'required': 'This field must not be empty'
            }
        }

        widgets = {
            # 'first_name': forms.TextInput(attrs={
            #    'placeholder': 'Type your name here...',}),
            # 'class': 'input text-input' #É possível add classe também

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here...'
            }),
        }
    # método clean_"alguma coisa" serve para o campo."

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid',
                params={'pipoca': '"atenção"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'})

        return data
    # método para validar o formulário como um todo

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal.', code='invalid')

            raise ValidationError({'password': password_confirmation_error,  # noqa E501
                                   'password2': [
                                       password_confirmation_error,
                                       # 'Another error',(Exemplo usado para saber que pode ser passado uma lista e pode passar string também)
                                   ]})

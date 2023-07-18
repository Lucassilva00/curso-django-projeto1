from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
            'email': 'The email must be valid'
        }

        # Altera as mensagens de erro
        error_messages = {
            'username': {
                'required': 'This field must not be empty'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your name here...',
                # 'class': 'input text-input' #É possível add classe também
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here...'
            }),
        }

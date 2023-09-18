from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your Username')
        add_placeholder(self.fields['email'], 'Your Email')
        add_placeholder(self.fields['first_name'],
                        'Type your first name...')
        add_placeholder(self.fields['last_name'],
                        'Type your last name...')
        add_placeholder(self.fields['password'], 'Type your password...')
        add_placeholder(self.fields['password2'], 'Repeat your password...')

    username = forms.CharField(
        error_messages={'required': 'This field must not be empty',
                        'min_length': 'Username must have at least 4 characters',  # noqa E501
                        'max_length': 'Username must have 150 characters or less'},  # noqa E501
        label='Username',
        help_text=('Username must have letters, numbers or one of those @.+-_. '  # noqa E501
            'The length should be between 4 and 150 characters.'),
        min_length=4,
        max_length=150,

    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name',
    )

    email = forms.EmailField(
        error_messages={'required': 'Type your email'},
        label='Email',
        help_text='The email must be valid',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label='Password2',
                                error_messages={
                                    'required': 'Please, repeat your password'}
                                )

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
        # Altera os help texts
        help_texts = {
            'password': 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'

        }

    # método clean_"alguma coisa" serve para o campo."

    # def clean_password(self):
    #    data = self.cleaned_data.get('password')
#
 #       if 'atenção' in data:
  #          raise ValidationError(
   #             'Não digite %(value)s no campo password',
    #            code='invalid',
     #           params={'value': '"atenção"'}
      #      )

       # return data

    # def clean_first_name(self):
     #   data = self.cleaned_data.get('first_name')
#
 #       if 'John Doe' in data:
  #          raise ValidationError(
   #             'Não digite %(value)s no campo first name',
    #            code='invalid',
     #           params={'value': '"John Doe"'})

      # return data
    # método para validar o formulário como um todo

    def clean_email(self):
        mail = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=mail).exists()

        if exists:
            raise ValidationError(
                'This e-mail is already in use.', code='invalid',
            )

        return mail

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
                                       # 'Another error',(Exemplo usado para saber que pode ser passado uma lista e pode passar string também) # noqa E501
                                   ]})

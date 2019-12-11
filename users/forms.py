from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    """
        Form for the login page.
        Unique email is used for the login
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'veuillez saisir votre email',
            'id': ''
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'mot de passe',
            'id': '',
        }
    ))
from django import forms
from django.contrib.auth import authenticate
from swift.models import User

#from swift.models import User


class SignInForm(forms.Form):
    email = forms.EmailField(
        label="Email", max_length=225,
        widget=forms.EmailInput( attrs={'class': 'effect', 'placeholder':'Enter your email'} ),
        error_messages={ 'required': 'The email should not be empty' }
    )
    password = forms.CharField(
        label="Password", max_length=50, min_length=1,
        widget= forms.PasswordInput( attrs={'class': 'effect', 'id': 'password', 'placeholder':'Enter the password'} ),
        error_messages={ 'required': 'The password should not be empty', 'min_length': 'The password strength should be 5 characters.' }
    )


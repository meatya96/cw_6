from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm
from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',
                             max_length=254,
                             widget=forms.EmailInput(attrs={
                                 'autocomplete': 'email',
                                 'class': 'form-control',
                                 'placeholder': 'Введите ваш email'}))
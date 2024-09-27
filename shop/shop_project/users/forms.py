from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from .tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите имя пользователя",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите пароль",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите имя пользователя",
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите имя",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите фамилию",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите адрес эл. почты",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Введите пароль",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control py-4",
                'placeholder': "Подтвердите пароль",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
                'readonly': True,
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control py-4",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'class': "form-control py-4",
                'readonly': True,
            }
        )
    )

    #
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': "custom-file-input",
            }
        ),
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

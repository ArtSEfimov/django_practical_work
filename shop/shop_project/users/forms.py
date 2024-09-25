from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User, EmailVerification
from django import forms
import uuid
from datetime import timedelta
from django.utils import timezone


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
        model = User
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
        expiration = timezone.now() + timedelta(hours=48)

        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
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
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

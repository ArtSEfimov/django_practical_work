from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.forms import ModelForm
from django import forms
from .models import Task, AdvancedProfile, Comments


class TaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')  # Получаем текущего пользователя
        super(TaskForm, self).__init__(*args, **kwargs)
        # Фильтруем поле allowed_users, исключая текущего пользователя
        self.fields['allowed_users'].queryset = get_user_model().objects.exclude(id=current_user.id)

    class Meta:
        model = Task
        exclude = ('status', 'creation_date', 'tags', 'user', 'complete_date')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your task title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter your task description'}),
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder': 'Select deadline'
            }
            ),
        }


class UserRegistration(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return super().clean_username()

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email


class UserImageForm(forms.ModelForm):
    delete_profile_image = forms.BooleanField(required=False, label='Удалить фото профиля', initial=False)

    class Meta:
        model = AdvancedProfile
        fields = ('profile_image', 'about')
        widgets = {
            'about': forms.Textarea(),
        }


class LoginUserForm(AuthenticationForm):
    username = UsernameField(label='Имя пользователя', widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class SearchTask(forms.Form):
    task = forms.CharField(label='Поиск задачи', initial='Найти задачу', empty_value=None)


class ChangePassForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Enter your comment'}),
        }

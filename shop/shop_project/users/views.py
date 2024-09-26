from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    title = 'Store - Регистрация'
    success_message = 'Вы успешно зарегистрировались!'


class UserProfileView(TitleMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = get_user_model().objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('index'))

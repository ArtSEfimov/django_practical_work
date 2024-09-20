from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, reverse, redirect
from .forms import CustomRegistrationForm
from .models import Notes


# Create your views here.


def show_registration_form(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = CustomRegistrationForm()
        return render(request, 'reg_site/registration.html', {'form': form})


def show_login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            clean_user_data = form.cleaned_data
            username = clean_user_data.get('username')
            password = clean_user_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('notes'))
            else:
                return redirect(reverse('login'))
    else:
        form = AuthenticationForm()
        return render(request, 'reg_site/login.html', {'form': form})


def show_notes(request):
    queryset = Notes.objects.filter(user=request.user)
    return render(request, 'reg_site/notes.html', {'notes': queryset})


def add_note(request):
    if request.method == 'POST':
        note_object = Notes()

        content = request.POST.get("note-text", None)
        if content:
            note_object.user = request.user
            note_object.note = content
            note_object.save()
        return redirect(reverse('notes'))

    return render(request, 'reg_site/add_form.html')

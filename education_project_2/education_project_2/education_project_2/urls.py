"""
URL configuration for education_project_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from reg_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', views.show_registration_form, name='registration'),
    path('login/', views.show_login_form, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('notes/', views.show_notes, name='notes'),
    path('add_note/', views.add_note, name='add_note')
]

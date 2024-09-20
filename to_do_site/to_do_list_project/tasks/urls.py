from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.ShowAllTasks.as_view(), name='all_tasks'),
    path('detail/<int:pk>/', views.DetailTask.as_view(), name='detail_task'),
    path('create/', views.CreateTask.as_view(), name='create_task'),
    path('edit/<int:pk>/', views.UpdateTask.as_view(), name='edit_task'),
    path('complete/<int:pk>/', views.check_done, name='complete_task'),
    path('delete/<int:pk>/', views.DeleteTask.as_view(), name='delete_task'),
    path('registration/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.UserLogiView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ShowUserProfile.as_view(), name='user_profile'),
    path('search/', views.SearchView.as_view(), name='search_task'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('edit_profile/', views.EditUserProfile.as_view(), name='edit_profile'),
    path('show_by_tags/<slug:slug>', views.ShowByTags.as_view(), name='show_by_tags'),

]

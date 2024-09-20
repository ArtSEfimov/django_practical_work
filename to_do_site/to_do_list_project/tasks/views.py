from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LogoutView, LoginView
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, FormView
from .forms import UserRegistration, LoginUserForm, SearchTask, ChangePassForm, UserImageForm, TaskForm, CommentsForm
from .models import Task, Tags, Comments
from django.shortcuts import render, get_object_or_404, redirect
from to_do_list_project import settings
from . import signals


# Create your views here.
class TagFilterMixin:
    def get_queryset(self):
        tag = Tags.objects.get(slug=self.kwargs.get('slug'))
        return super().get_queryset().filter(tags=tag)


class AllowedUsersMixin:
    def get_object(self):
        try:
            super_object = super().get_object()
        except Http404:

            queryset = self.request.user.tasks_for_allowed_users.all()
            super_object = super().get_object(queryset=queryset)
        return super_object


class AuthorizedUserMixin:
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Task.objects.none()

        return super().get_queryset().filter(user=self.request.user)


class ShowAllTasks(AuthorizedUserMixin, ListView):
    model = Task
    template_name = 'tasks/to_do_list.html'
    context_object_name = 'tasks'
    ordering = ['creation_date']
    extra_context = {'search_form': SearchTask(), 'status': ''}

    def __init__(self, *args, **kwargs):
        signals.my_email_sender()
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_key = self.request.GET.get('sort_key', None)
        if sort_key:
            queryset = queryset.order_by(sort_key)
            if sort_key.endswith('priority'):
                queryset = sorted(queryset, key=lambda x: x.priority is None)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):
            another_tasks = self.request.user.tasks_for_allowed_users.all()
            another_sort_key = self.request.GET.get('another_sort_key', None)
            if another_sort_key:
                another_tasks = another_tasks.order_by(another_sort_key)
            else:
                another_tasks = another_tasks.order_by('creation_date')

            context.update({'another_tasks': another_tasks})

        return context


class CreateTask(CreateView):
    template_name = 'tasks/forms/add_task_form.html'
    success_url = reverse_lazy('tasks:all_tasks')
    form_class = TaskForm

    def __init__(self, *args, **kwargs):
        self.tag_set = set()
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Добавляем текущего пользователя
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        form.instance.tags.add(*Tags.objects.filter(tag__in=self.tag_set))

        return response

    def post(self, request, *args, **kwargs):

        custom_tags = request.POST.get('custom_tags', None)
        if custom_tags:
            db_tags = Tags.objects.all()
            for tag in custom_tags.split(','):
                tag = tag.strip().lower()
                if db_tags.exists():
                    tag_from_db = db_tags.filter(tag=tag)
                    if not tag_from_db:
                        Tags.objects.create(tag=tag)
                        self.tag_set.add(tag)
                    else:
                        self.tag_set.add(tag)
                else:
                    current_tag = Tags.objects.create(tag=tag)
                    self.tag_set.add(current_tag)

        db_tags = request.POST.getlist('db_tags', None)

        if db_tags:
            for t in db_tags:
                self.tag_set.add(t)

        return super().post(request, *args, **kwargs)


class UpdateTask(AuthorizedUserMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/forms/add_task_form.html'
    success_url = reverse_lazy('tasks:all_tasks')

    def __init__(self, *args, **kwargs):
        self.tag_set = set()
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Добавляем текущего пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        object_tags = self.get_object().tags.all()
        context = super().get_context_data(**kwargs)
        context.update({'selected_tags': object_tags})
        return context

    def processing_tags(self, request):
        custom_tags = request.POST.get('custom_tags', None)
        if custom_tags:
            db_tags = Tags.objects.all()
            for tag in custom_tags.split(','):
                tag = tag.strip().lower()
                if db_tags.exists():
                    tag_from_db = db_tags.filter(tag=tag)
                    if not tag_from_db:
                        Tags.objects.create(tag=tag)
                        self.tag_set.add(tag)
                    else:
                        self.tag_set.add(tag)
                else:
                    current_tag = Tags.objects.create(tag=tag)
                    self.tag_set.add(current_tag)

        db_tags = request.POST.getlist('db_tags', None)

        if db_tags:
            for t in db_tags:
                self.tag_set.add(t)

    def post(self, request, *args, **kwargs):

        self.processing_tags(request)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        form.instance.tags.clear()
        form.instance.tags.add(*Tags.objects.filter(tag__in=self.tag_set))

        return response


def check_done(request, pk):
    current_task = get_object_or_404(Task, pk=pk)

    if request.POST['task_status'] == "1":
        current_task.status = 1
    else:
        current_task.status = 0
    current_task.save()

    return redirect(reverse('tasks:all_tasks'))


class DeleteTask(AuthorizedUserMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:all_tasks')

    def get(self, request, *args, **kwargs):
        obj_for_delete = self.get_object()
        title = obj_for_delete.title
        obj_for_delete.delete()
        messages.info(request, f'задача {title} успешно удалена')
        return redirect(self.success_url)


class DetailTask(AuthorizedUserMixin, AllowedUsersMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/detail_task.html'

    def __init__(self, *args, **kwargs):
        self.context_form = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = self.get_object().tags.all()
        context.update({'tags': tags})

        context.update({'form_comment': CommentsForm()})

        if self.context_form is not None:
            context.update({'form_comment': self.context_form})

        comments = Comments.objects.filter(task=self.get_object())
        context.update({'comments': comments})

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CommentsForm(request.POST)
            if form.is_valid():
                model_object = form.save(commit=False)
                model_object.creator_user = request.user
                model_object.task = self.get_object()
                model_object.save()

                referer_url = request.META.get('HTTP_REFERER', '/')

                return redirect(referer_url)

            self.context_form = form

        return super().dispatch(request, *args, **kwargs)


class RegisterUser(CreateView):
    template_name = 'tasks/user/registration.html'
    success_url = reverse_lazy('tasks:login')

    def post(self, request, *args, **kwargs):
        user_form = UserRegistration(request.POST)
        user_image_form = UserImageForm(request.POST, request.FILES)

        if user_form.is_valid():
            if user_image_form.is_valid():
                user_form_object = user_form.save(commit=False)
                user_form_object.user = request.user
                user_form_object.save()

                user_image_form_object = user_image_form.save(commit=False)
                user_image_form_object.user = user_form_object

                user_image_form_object.save()

                return redirect(self.success_url)

        return render(request, self.template_name,
                      {'user_form': user_form, 'user_image_form': user_image_form})

    def get(self, request, *args, **kwargs):
        user_form = UserRegistration()
        user_image_form = UserImageForm()

        return render(request, self.template_name,
                      {'user_form': user_form, 'user_image_form': user_image_form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('tasks:all_tasks')  # URL, на который вы хотите перенаправить пользователя после выхода


class ShowUserProfile(DetailView):
    model = get_user_model()
    template_name = 'tasks/user/user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(user=self.request.user)

        tasks_count = tasks.count()
        context['tasks'] = tasks_count

        completed_tasks = tasks.filter(status=1).count()
        context['completed_tasks'] = completed_tasks

        return context

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


class UserLogiView(LoginView):
    template_name = 'tasks/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('tasks:all_tasks')


class SearchView(AuthorizedUserMixin, ListView):
    model = Task
    template_name = 'tasks/to_do_list.html'
    session_dict = dict()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            if self.session_dict:
                queryset = self.session_dict['queryset']
                sort_key = self.request.GET.get('sort_key', None)
                if sort_key:
                    queryset = queryset.order_by(sort_key)
                context.update({'tasks': queryset})
        return context

    def post(self, *args, **kwargs):
        form = SearchTask(self.request.POST)
        self.session_dict.clear()
        if form.is_valid():
            task = form.cleaned_data['task']
            status = self.request.POST.get('radio_status', '')
        else:
            return render(self.request, 'tasks/to_do_list.html')
        if task:
            queryset = super().get_queryset().filter(Q(title__icontains=task) | Q(description__icontains=task))
            if status:
                queryset = queryset.filter(status=int(status))
            if queryset:
                self.session_dict['queryset'] = queryset

                return render(self.request, 'tasks/to_do_list.html',
                              context={'tasks': queryset, 'status': status, 'is_search': True})
        if status:
            show_status = dict(self.model.TASK_STATUS)[int(status)]
            messages.success(self.request, f'Найдены задачи со статусом {show_status}')
            queryset = super().get_queryset().filter(status=int(status))

            self.session_dict['queryset'] = queryset

            return render(self.request, 'tasks/to_do_list.html',
                          context={'tasks': queryset, 'status': status, 'is_search': True})

        messages.info(self.request, 'По вышему запросу ничего не найдено')
        return redirect(reverse('tasks:all_tasks'))


class ChangePassword(FormView):
    form_class = ChangePassForm
    success_url = reverse_lazy('tasks:all_tasks')
    template_name = 'tasks/user/change_password.html'

    def form_valid(self, form):

        user = authenticate(self.request,
                            username=self.request.user,
                            password=form.cleaned_data['old_password'])

        if user:
            tmp_user = authenticate(self.request,
                                    username=self.request.user,
                                    password=form.cleaned_data['new_password1'])
            if tmp_user:
                form.add_error(None, 'Новый пароль совпадает со старым')
                return self.form_invalid(form)

            if form.cleaned_data['new_password1'] == form.cleaned_data['new_password2']:

                user.set_password(form.cleaned_data['new_password1'])

                messages.success(self.request, 'Пароль успешно изменен')
                user.save()

                login(self.request, user)

                return super().form_valid(form)

            else:
                form.add_error(None, 'Пароли не совпадают')
        else:
            form.add_error(None, 'Неверный пароль')

        return self.form_invalid(form)


class EditUserProfile(FormView):
    template_name = 'tasks/user/edit_profile.html'
    success_url = reverse_lazy('tasks:user_profile')

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_form = UserRegistration(instance=current_user)
        user_advanced_form = UserImageForm(instance=current_user.advancedprofile)

        user_form.fields['email'].disabled = True
        user_form.fields['username'].disabled = True

        return render(request, self.template_name,
                      {'user_form': user_form, 'user_advanced_form': user_advanced_form})

    def post(self, request, *args, **kwargs):
        user = request.user
        instance = user.advancedprofile
        user_advanced_form = UserImageForm(request.POST, request.FILES, instance=instance)

        if user_advanced_form.is_valid():

            if user_advanced_form.cleaned_data.get('delete_profile_image'):
                instance.profile_image.delete(save=False)  # Удаляем изображение из файловой системы
                instance.profile_image = None  # Устанавливаем поле в None

            user_advanced_form.save()

            return redirect(self.success_url)

        user_form = UserRegistration(instance=user)
        return render(request, self.template_name,
                      {'user_form': user_form, 'user_advanced_form': user_advanced_form})


class ShowByTags(AuthorizedUserMixin, TagFilterMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_by_slug.html'
    context_object_name = 'tasks'
    ordering = ['creation_date']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tags.objects.get(slug=self.kwargs.get('slug'))
        context.update({'tag_title': tag})
        return context

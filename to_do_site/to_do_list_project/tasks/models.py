from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    TASK_STATUS = [
        (1, 'completed'),
        (0, 'not completed')
    ]

    class Priority(models.IntegerChoices):
        HIGH = 3, 'high priority'
        MIDDLE = 2, 'middle priority'
        LOW = 1, 'low priority'

    title = models.CharField(verbose_name='Название задачи', max_length=100, blank=False, null=False)
    description = models.TextField(verbose_name='Описание задачи')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(choices=TASK_STATUS, default=0, null=False)
    complete_date = models.DateTimeField(default=None, null=True, blank=True, verbose_name='Дата завершения')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(to='Tags', blank=True)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=None, blank=True, null=True)
    allowed_users = models.ManyToManyField(get_user_model(), blank=True, related_name='tasks_for_allowed_users')
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(
            self,
            *args,
            **kwargs,
    ):
        if self.pk:  # значит объект уже есть в БД и ему присвоен pk
            old_object = self.__class__.objects.get(pk=self.pk)
            if old_object.status == 0 and self.status == 1:
                self.complete_date = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tasks:detail_task', args=(str(self.pk),))


class AdvancedProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image',
                                      null=True,
                                      blank=True,
                                      verbose_name='Изображение профиля',
                                      help_text='Загрузите изображение вашего профиля')
    about = models.TextField(null=True, blank=True)


class Tags(models.Model):
    tag = models.CharField(max_length=50, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tasks:show_by_tags', args=(self.slug,))

    def __str__(self):
        return self.tag


class Comments(models.Model):
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    creator_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)

from django.db.models.signals import pre_save
from django.dispatch import receiver
from slugify import slugify
from .models import Tags, Task
from to_do_list_project import settings
from django.core.mail import send_mail
from django.utils import timezone


@receiver(pre_save, sender=Tags)
def update_complete_date(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.tag)


def my_email_sender():
    if not settings.IS_EMAIL_SENT:
        users = []
        for d in Task.objects.all():
            if d.deadline:
                if d.deadline < timezone.now():
                    users.append(
                        {'task': d,
                         'user': d.user
                         }
                    )
                    print(d.deadline - timezone.now())
        for task_user in users:
            task = task_user['task']
            user = task_user['user']
            user_email = user.email
            print(f'Send email to {user} on {user_email} about {task}')
        print('Sending email...')

    # send_mail(
    #     'Subject here',  # Тема сообщения
    #     'Here is the message.',  # Тело сообщения
    #     settings.EMAIL_HOST_USER,  # Адрес отправителя
    #     (settings.EMAIL_HOST_USER,),  # Список адресов получателей
    #     fail_silently=False,  # Если True, ошибки отправки будут проигнорированы
    # )
    settings.IS_EMAIL_SENT = True

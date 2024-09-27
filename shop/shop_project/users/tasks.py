import uuid
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import EmailVerification


@shared_task
def send_email_verification(user_id):
    user = get_user_model().objects.get(pk=user_id)
    expiration = timezone.now() + timedelta(hours=48)

    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()

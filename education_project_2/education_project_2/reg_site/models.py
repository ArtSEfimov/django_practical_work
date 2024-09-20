from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    pass


class Notes(models.Model):
    note = models.TextField()
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

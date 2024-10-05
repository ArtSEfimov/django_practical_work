from django.db import models


class TaskModel(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    is_complete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title

from django.contrib import admin
from .models import Task, Tags


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

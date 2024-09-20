from django.contrib.auth.models import AnonymousUser

from .models import Tags


def tag_processor(request):
    actual_tags = set()

    if not isinstance(request.user, AnonymousUser):
        tags = Tags.objects.all()
        for tag in tags:
            if tag.task_set.filter(user=request.user).exists():
                actual_tags.add(tag)

    return {'actual_tags': actual_tags}


def all_db_tags(request):
    return {'all_db_tags': Tags.objects.all()}

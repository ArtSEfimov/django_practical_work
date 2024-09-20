from django import template

register = template.Library()


@register.filter
def get_picture(my_user):
    if hasattr(my_user, 'AdvancedProfile'.lower()):
        return my_user.advancedprofile.profile_image


@register.simple_tag
def about_include(my_user):
    if hasattr(my_user, 'AdvancedProfile'.lower()):
        return my_user.advancedprofile.about


@register.filter
def sort_task_collection(queryset, key):
    return sorted(queryset, key=lambda x: x.key if hasattr(x, key) else 0)

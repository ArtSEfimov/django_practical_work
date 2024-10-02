from django.contrib import admin
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from general.filters import AuthorFilter, PostFilter
from general.models import User, Post, Reaction, Comment
from django.contrib.auth.models import Group
from rangefilter.filters import DateRangeFilter

admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    fields = (
        "first_name",
        "last_name",
        "username",
        "password",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "friends",
        "date_joined",
        "last_login",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    search_fields = (
        "id",
        "username",
        "email",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        ("date_joined", DateRangeFilter),
    )


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "get_body",
        "created_at",
        'get_comment_count',
    )

    readonly_fields = (
        "created_at",
    )

    search_fields = (
        "id",
        "title",
    )

    list_filter = (
        AuthorFilter,
        ("created_at", DateRangeFilter),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")

    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body

    get_body.short_description = "body"

    def get_comment_count(self, obj):
        return obj.comments.count()

    get_comment_count.short_description = 'comments'

    list_display_links = (
        "id",
        "get_body",
        "title",
    )


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "value",
    )

    list_filter = (
        PostFilter,
        AuthorFilter,
        ("value", ChoiceDropdownFilter),
    )

    autocomplete_fields = (
        "author",
        "post",
    )


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "body",
        "created_at",
    )

    list_display_links = (
        "id",
        "body",
    )

    list_filter = (
        PostFilter,
        AuthorFilter,
    )

    raw_id_fields = (
        "author",
    )

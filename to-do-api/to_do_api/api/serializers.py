import json

from rest_framework import serializers

from api.models import TaskModel


class TaskSerializer:
    def __init__(self, task_object):
        self.task_object = task_object

    def to_dict(self):
        current_dict = {}
        for field in self.task_object.__class__._meta.get_fields():
            if not field.auto_created:  # Исключаем автоматические поля
                field_name = field.name
                if field.is_relation:
                    related_object = getattr(self.task_object, field_name)
                    current_dict[field_name] = related_object.id if related_object else None
                else:
                    current_dict[field_name] = getattr(self.task_object, field_name)

        return current_dict

    def to_json(self):
        # Сначала получаем словарь данных
        task_dict = self.to_dict()

        # Преобразуем словарь в JSON
        task_json = json.dumps(task_dict, ensure_ascii=False, indent=4)

        return task_json


class TaskPOSTSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    is_complete = serializers.BooleanField(default=False, required=False)

    def create(self, validated_data):
        TaskModel.objects.create(**validated_data)
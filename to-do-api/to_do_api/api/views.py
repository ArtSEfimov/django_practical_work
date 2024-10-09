import json

from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet

from api.models import TaskModel
from api.serializers import TaskSerializer, TaskPOSTSerializer


class TaskAPIView(APIView):
    http_method_names = ['get']

    def get(self, request, pk=None):
        if pk:
            task_object = get_object_or_404(TaskModel, pk=pk)
            return HttpResponse(TaskSerializer(task_object).to_json(),
                                content_type='application/json')

        task_objects = TaskModel.objects.all()
        serialized_objects = []
        for task_objects in task_objects:
            serialized_objects.append(TaskSerializer(task_objects).to_dict())

        return HttpResponse(json.dumps(serialized_objects),
                            content_type='application/json')


class TaskCreateAPIView(ViewSet):

    def create(self, request):
        serialized_data = TaskPOSTSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(serialized_data.data)

    def retrieve(self, request, pk):
        pass


class TaskViewSet(GenericViewSet):
    pass

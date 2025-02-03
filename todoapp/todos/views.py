from rest_framework.viewsets import ModelViewSet

from .serializers import TodoSerializer, TodoUpdateSerializer
from .models import Todo


class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    def get_serializer_class(self):
        if self.action == 'create':
            return TodoSerializer
        elif self.action == 'update' or self.action == 'retrieve':
            return TodoUpdateSerializer
        return TodoSerializer

    def perform_update(self, serializer):
        todo_instance = self.get_object()
        todo_data = self.request.data
        todo = todo_data.get('task_name')
        done = todo_data.get('done')

        if todo:
            todo_instance.name = todo
        if done is not None:
            todo_instance.done = done

        todo_instance.save()
        serializer.save()

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Todo.objects.filter(user__id=user_id)
        return Todo.objects.all()

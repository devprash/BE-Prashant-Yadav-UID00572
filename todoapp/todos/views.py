from rest_framework.viewsets import ModelViewSet

from todos import (
    models as todo_models,
    serializers as todo_serializers
)


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
        serializer = None
        if self.action == 'create':
            serializer = todo_serializers.TodoSerializerForAPI
        else:
            serializer = todo_serializers.TodoUpdateSerializer

        return serializer

    def get_queryset(self):
        queryset = None
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = todo_models.Todo.objects.filter(user__id=user_id)
        else:
            queryset = todo_models.Todo.objects.all()
            
        return queryset

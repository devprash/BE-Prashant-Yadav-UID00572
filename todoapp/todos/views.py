from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer = None
        if self.action == 'create':
            serializer = todo_serializers.TodoSerializerForAPI
        else:
            serializer = todo_serializers.TodoUpdateSerializer

        return serializer

    def get_queryset(self):
        queryset = None
        user = self.request.user
        if user.is_authenticated:
            queryset = todo_models.Todo.objects.filter(user=user)

        return queryset

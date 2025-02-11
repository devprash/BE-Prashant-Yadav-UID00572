from rest_framework import serializers

from todos import (
    models as todo_models
)
from users import (
    models as user_models,
    serializers as user_serializers
)


class TopFiveWithPendingTodoSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class TodoDateRangeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y')

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = todo_models.Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class TodoSerializer(serializers.ModelSerializer):
    creator = user_serializers.UserSerializerWithoutIdField(source="user")
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y')

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    class Meta:
        model = todo_models.Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']


class TodoSerializerForAPI(serializers.ModelSerializer):
    task_name = serializers.CharField(source="name")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    class Meta:
        model = todo_models.Todo
        fields = ['task_name', 'done',
                  'date_created']


class TodoUpdateSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(source="name")
    todo_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = todo_models.Todo
        fields = ['todo_id', 'task_name', 'done']

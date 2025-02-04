from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users import (
    models as user_models
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserSerializerWithoutIdField(serializers.ModelSerializer):
    class Meta:
        model = user_models.CustomUser
        fields = ['first_name', 'last_name', 'email']


class UserPendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class UserProjectSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField()
    in_progress_projects = serializers.ListField()
    completed_projects = serializers.ListField()

    class Meta:
        model = user_models.CustomUser
        fields = ["first_name", "last_name", "email",
                  "to_do_projects", "in_progress_projects", "completed_projects"]

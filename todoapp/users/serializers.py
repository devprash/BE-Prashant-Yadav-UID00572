from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserSerializerWithoutIdField(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class UserPendingTodosSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class UserProjectSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.SerializerMethodField()
    in_progress_projects = serializers.SerializerMethodField()
    completed_projects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email",
                  "to_do_projects", "in_progress_projects", "completed_projects"]

    def get_to_do_projects(self, obj):
        return obj.to_do if obj.to_do else []

    def get_in_progress_projects(self, obj):
        return obj.in_progress if obj.in_progress else []

    def get_completed_projects(self, obj):
        return obj.completed if obj.completed else []

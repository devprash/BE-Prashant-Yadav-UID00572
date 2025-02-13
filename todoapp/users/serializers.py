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
        fields = [
            "first_name", "last_name", "email",
            "to_do_projects", "in_progress_projects",
            "completed_projects"
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = user_models.CustomUser
        fields = ['email', 'password', 'first_name',
                  'last_name', 'date_joined']
        read_only_fields = ['date_joined']

    def validate_email(self, value):
        if user_models.CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def create(self, validated_data):
        user = user_models.CustomUser.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

from rest_framework import serializers

from projects import (
    models as project_models
)
from users import (
    models as user_models
)


class ProjectWithMemberName(serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.CharField(source="name")

    def get_done(self, obj):
        return True if obj.status == 2 else False

    class Meta:
        model = project_models.Project
        fields = ['project_name', 'done', 'max_members']


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    existing_member_count = serializers.IntegerField()

    class Meta:
        model = project_models.Project
        fields = ["id", "name", "status",
                  "existing_member_count", "max_members"]

    def get_status(self, obj):
        return obj.CHOICES[obj.status][1]


class UserReportSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()
    completed_count = serializers.IntegerField()

    class Meta:
        model = user_models.CustomUser
        fields = ["first_name", "last_name", "email",
                  "pending_count", "completed_count"]


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="name")
    report = UserReportSerializer(source="reports", many=True, read_only=True)

    class Meta:
        model = project_models.Project
        fields = ['project_title', 'report']

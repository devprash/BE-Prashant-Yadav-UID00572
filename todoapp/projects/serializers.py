from rest_framework import serializers
from projects.models import Project


class ProjectWithMemberName(serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.CharField(source="name")

    def get_done(self, obj):
        if (obj.status == 0 or obj.status == 1):
            return False
        else:
            return True

    class Meta:
        model = Project
        fields = ['project_name', 'done', 'max_members']


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    existing_member_count = serializers.IntegerField()

    class Meta:
        model = Project
        fields = ["id", "name", "status",
                  "existing_member_count", "max_members"]

    def get_status(self, obj):
        if (obj.status == 0):
            return "To be started"
        elif (obj.status == 1):
            return "In progress"
        else:
            return "Completed"


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="name")
    report = serializers.SerializerMethodField()

    def get_report(self, obj):
        user_reports = []
        for user in obj.reports:
            user_report = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "pending_count": user.pending_count,
                "completed_count": user.completed_count
            }
            user_reports.append(user_report)
        return user_reports

    class Meta:
        model = Project
        fields = ['project_title', 'report']

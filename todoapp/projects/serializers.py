from django.db.models import Count

from rest_framework import serializers

from projects import (
    models as project_models
)
from users import (
    models as user_models
)

from django.db import connection

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
        return obj.get_status_display()


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


class ProjectMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
    action = serializers.CharField()

    class Meta:
        fields = ['user_ids', 'action']

    def validate_action(self, value):
        if value not in ['add', 'remove']:
            raise serializers.ValidationError(
                'Action should either be add or remove.')
        return value

    def validate(self, validated_data):
        user_ids = validated_data['user_ids']
        project_id = self.context['project_id']
        action = validated_data['action']
        project = project_models.Project.objects.get(id=project_id)
        logs = {}
        invalid_users = set(
            user_id for user_id in user_ids if not user_models.CustomUser.objects.filter(id=user_id).exists()
        )
        if invalid_users:
            for user_id in invalid_users:
                logs[user_id] = 'User does not exist.'

        if action == 'add':
            valid_users = []
            user_project_counts = {
                user_id: count for user_id, count in project_models.ProjectMember.objects
                .filter(member_id__in=user_ids)
                .values_list('member_id')
                .annotate(count=Count('project'))
            }
            existing_members = set(
                project_models.ProjectMember.objects.filter(project=project)
                .values_list('member_id', flat=True)
            )
            remaining_slots = project.max_members - project_models.ProjectMember.objects.filter(
                project=project).count()
            for user_id in user_ids:
                if user_id in existing_members:
                    logs[user_id] = 'User is already a member of this project.'
                elif user_project_counts.get(user_id, 0) >= 2:
                    logs[user_id] = 'Cannot add user as they are already in two projects.'
                elif remaining_slots <= 0:
                    logs[user_id] = 'Project has reached its maximum member count.'
                elif user_id in invalid_users:
                    continue
                else:
                    logs[user_id] = 'Successfully added to the project.'
                    valid_users.append(user_id)
                    remaining_slots -= 1
            self.context['valid_users'] = valid_users
        elif action == 'remove':
            existing_members = set(
                project_models.ProjectMember.objects.filter(project=project)
                .values_list('member_id', flat=True)
            )
            valid_users = []
            for user_id in user_ids:
                if user_id not in existing_members:
                    logs[user_id] = 'User is not a member of this project.'
                else:
                    logs[user_id] = 'Successfully removed from the project.'
                    valid_users.append(user_id)

            self.context['valid_users'] = valid_users
        self.context['logs'] = logs

        return validated_data

    def save(self):
        project_id = self.context['project_id']
        project = project_models.Project.objects.get(id=project_id)
        valid_users = self.context['valid_users']
        action = self.validated_data['action']
        logs = self.context['logs']

        if action == 'add':
            new_members = [
                project_models.ProjectMember(
                    project=project, member_id=user_id)
                for user_id in valid_users
            ]
            project_models.ProjectMember.objects.bulk_create(new_members)
        elif action == 'remove':
            project_models.ProjectMember.objects.filter(
                member_id__in=valid_users).delete()
            
        print(f'\n LINE148: Connection Queries: {len(connection.queries)}  \n')
        return {'logs': logs}

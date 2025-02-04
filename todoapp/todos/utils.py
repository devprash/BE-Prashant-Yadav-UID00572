import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Case, Count, IntegerField, Prefetch, Q, When

from projects import (
    models as project_models,
    serializers as project_serializers
)
from todos import (
    models as todo_models,
    serializers as todo_serializers
)
from users import (
    models as user_models,
    serializers as user_serializers
)

# from users.serializers import UserProjectSerializer, UserSerializer

# Add code to this util to return all users list in specified format.
# [ {
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com"
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_all_users():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of users data
    """
    users = user_models.CustomUser.objects.all()
    serializer = user_serializers.UserSerializer(users, many=True)

    return serializer.data


# Add code to this util to  return all todos list (done/to do) along with user details in specified format.
# [{
#   "id": 1,
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Dec, 2021"
#   "creator" : {
#       "first_name": "Amal",
#       "last_name": "Raj",
#       "email": "amal.raj@joshtechnologygroup.com",
#   }
# },
# {
#   "id": 2,
#   "name": "Complete Python Assignment",
#   "status": "To Do",
#   "created_at": "5:30 PM, 13 Dec, 2021",
#   "creator" : {
#      "first_name": "Gurpreet",
#       "last_name": "Singh",
#       "email": "gurpreet.singh@joshtechnologygroup.com",
#   }
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_all_todo_list_with_user_details():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of todos
    """
    todos = todo_models.Todo.objects.select_related('user').all()
    serializer = todo_serializers.TodoSerializer(todos, many=True)

    return serializer.data


# Add code to this util to return all projects with following details in specified format.
# [{
#   "id": 1,
#   "name": "Project A",
#   "status": "Done",
#   "existing_member_count": 4,
#   "max_members": 5
# },
# {
#   "id": 2,
#   "name": "Project C",
#   "status": "To Do",
#   "existing_member_count": 2,
#   "max_members": 4
# }]
# Note: use serializer for generating this format. use source for status in serializer field.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_projects_details():
    """
    Util to fetch all project details
    :return: list of dicts - List of project with details
    """
    projects = project_models.Project.objects.annotate(
        existing_member_count=Count("projectmember")
    )
    serializer = project_serializers.ProjectSerializer(projects, many=True)

    return json.loads(json.dumps(serializer.data))


# Add code to this util to  return stats (done & to do count) of all users in specified format.
# [{
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "completed_count": 3,
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com",
#   "completed_count": 5,
#   "pending_count": 0
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_users_todo_stats():
    """
    Util to fetch todos list stats of all users on platform
    :return: list of dicts -  List of users with stats
    """
    users = user_models.CustomUser.objects.annotate(
        completed_count=Count(
            Case(
                When(todo__done=True, then=1),
                output_field=IntegerField()
            )
        ),
        pending_count=Count(
            Case(
                When(todo__done=False, then=1),
                output_field=IntegerField()
            )
        )
    ).values("id", "first_name", "last_name", "email", "completed_count", "pending_count")

    return json.loads(json.dumps(list(users)))

# Add code to this util to return top five users with maximum number of pending todos in specified format.
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 10
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_five_users_with_max_pending_todos():
    """
    Util to fetch top five user with maximum number of pending todos
    :return: list of dicts -  List of users
    """
    top_five_user = user_models.CustomUser.objects.annotate(
        pending_count=Count('todo', filter=Q(todo__done=False))
    ).order_by("-pending_count")[:5]
    serialized_data = todo_serializers.TopFiveWithPendingTodoSerializer(
        top_five_user, many=True)

    return json.loads(json.dumps(serialized_data.data))

# Add code to this util to return users with given number of pending todos in specified format.
# e.g where n=4
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint : use annotation and aggregations


def fetch_users_with_n_pending_todos(n):
    """
    Util to fetch top five user with maximum number of pending todos
    :param n: integer - count of pending todos
    :return: list of dicts -  List of users
    """
    users = user_models.CustomUser.objects.annotate(
        pending_count=Count(
            Case(
                When(todo__done=False, then=1),
                output_field=IntegerField()
            )
        )
    ).filter(pending_count=n)
    serialized_data = todo_serializers.TopFiveWithPendingTodoSerializer(
        users, many=True)

    return json.loads(json.dumps(serialized_data.data))


# Add code to this util to return todos that were created in between given dates (add proper order too) and marked as
# done in specified format.
#  e.g. for given range - from 12-01-2021 to 12-02-2021
# [{
#   "id": 1,
#   "creator": "Amal Raj"
#   "email": "amal.raj@joshtechnologygroup.com"
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Jan, 2021"
# },
# {
#   "id": 2,
#   "creator": "Nikhil Khurana"
#   "email": "nikhil.khurana@joshtechnologygroup.com"
#   "name": "Complete Python Assignment",
#   "status": "Done",
#   "created_at": "5:30 PM, 02 Feb, 2021"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_completed_todos_with_in_date_range(start, end):
    """
    Util to fetch todos that were created in between given dates and marked as done.
    :param start: string - Start date e.g. (12-01-2021)
    :param end: string - End date e.g. (12-02-2021)
    :return: list of dicts - List of todos
    """
    start_date = datetime.strptime(start, "%d-%m-%Y")
    end_date = datetime.strptime(end, "%d-%m-%Y")
    todos = todo_models.Todo.objects.select_related('user').filter(
        date_created__range=[start_date, end_date],
        done=True
    )
    serializer = todo_serializers.TodoDateRangeSerializer(todos, many=True)

    return json.loads(json.dumps(serializer.data))


# Add code to this util to return list of projects having members who have name either starting with A or ending with A
# (case-insensitive) in specified format.
# [{
#   "project_name": "Project A"
#   "done": False
#   "max_members": 3
#   },
#   {
#   "project_name": "Project B"
#   "done": False
#   "max_members": 3
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_project_with_member_name_start_or_end_with_a():
    """
    Util to fetch project details having members who have name either starting with A or ending with A.
    :return: list of dicts - List of project data
    """
    projects = project_models.Project.objects.filter(
        Q(members__first_name__istartswith='A') | Q(
            members__last_name__iendswith='A')
    ).distinct()
    serializer = project_serializers.ProjectWithMemberName(projects, many=True)

    return json.loads(json.dumps(serializer.data))

# Add code to this util to return project wise todos stats per user in specified format.
# [{
#   "project_title": "Project A"
#   "report": [
#       {
#           "first_name": "Amal",
#           "last_name": "Raj",
#           "email": "amal.raj@joshtechnologygroup.com",
#           "pending_count": 1,
#           "completed_count": 1,
#       },
#       {
#           "first_name": "Nikhil",
#           "last_name": "Khurana",
#           "email": "nikhil.khurana@joshtechnologygroup.com",
#           "pending_count": 0,
#           "completed_count": 5,
#       }
#   ]
# },
# {
#   "project_title": "Project B"
#   "report": [
#       {
#           "first_name": "Gurpreet",
#           "last_name": "Singh",
#           "email": "gurpreet.singh@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 15,
#       },
#       {
#           "first_name": "Naveen",
#           "last_name": "Kumar",
#           "email": "naveenk@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 5,
#       }
#   ]
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.


def fetch_project_wise_report():
    """
    Util to fetch project wise todos pending &  count per user.
    :return: list of dicts - List of report data
    """
    members_prefetch = Prefetch(
        'members',
        user_models.CustomUser.objects.annotate(
            pending_count=Count(
                Case(
                    When(todo__done=False, then=1),
                    output_field=IntegerField()
                )
            ),
            completed_count=Count(
                Case(
                    When(todo__done=True, then=1),
                    output_field=IntegerField()
                )
            )
        ).order_by("email"),
        to_attr='reports'
    )
    project_data = project_models.Project.objects.prefetch_related(
        members_prefetch
    )
    serialized_data = project_serializers.ProjectReportSerializer(
        project_data, many=True)

    return json.loads(json.dumps(serialized_data.data))


# Add code to this util to return all users project stats in specified format.
# [{
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project A", "Project C"],
#       "in_progress": ["Project B", "Project E"],
#       "completed": ["Project R", "Project L"],
#   }
# },
# {
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project C"],
#       "in_progress": ["Project B", "Project F"],
#       "completed": ["Project K", "Project L"],
#   }
# }]
# Note: Use serializer for generating this format
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint: Use subquery/aggregation for project data.
def fetch_user_wise_project_status():
    """
    Util to fetch user wise project statuses.
    :return: list of dicts - List of user project data
    """
    users = user_models.CustomUser.objects.annotate(
        to_do_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=project_models.Project.Status.STATUS_TO_BE_STARTED)
        ),
        in_progress_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=project_models.Project.Status.STATUS_IN_PROGRESS)
        ),
        completed_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=project_models.Project.Status.STATUS_COMPLETED)
        )
    )
    serializer = user_serializers.UserProjectSerializer(users, many=True)

    return json.loads(json.dumps(serializer.data))

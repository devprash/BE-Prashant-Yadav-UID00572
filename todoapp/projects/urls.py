from django.urls import include, path

from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

urlpatterns=[
    path('<int:id>/', ProjectMemberApiViewSet.as_view()),
]

from django.urls import path

from .views import JobDetail, JobList

app_name = "jobs"
urlpatterns = [
    path("", JobList.as_view(), name="list"),
    path("<int:pk>", JobDetail.as_view(), name="detail"),
]

from django.urls import path

from .views import CourseDetailView, CourseListView

app_name = "learning"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path(
        "courses/<int:course_id>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
]
from django.urls import path

from .views import CourseCreateView, CourseDetailView, CourseListView

app_name = "learning"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/create/", CourseCreateView.as_view(), name="course-create"),
    path(
        "courses/<int:course_id>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
]
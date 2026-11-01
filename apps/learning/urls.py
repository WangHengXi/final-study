from django.urls import path

from .views import (
    ChapterCreateView,
    CourseCreateView,
    CourseDetailView,
    CourseListView,
    QuestionCreateView,
    CourseSettingUpdateView,
)

app_name = "learning"

urlpatterns = [
    path(
        "courses/",
        CourseListView.as_view(),
        name="course-list",
    ),
    path(
        "courses/create/",
        CourseCreateView.as_view(),
        name="course-create",
    ),
    path(
        "courses/<int:course_id>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path(
        "courses/<int:course_id>/chapters/create/",
        ChapterCreateView.as_view(),
        name="chapter-create",
    ),
    path(
        "chapters/<int:chapter_id>/questions/create/",
        QuestionCreateView.as_view(),
        name="question-create",
    ),
    path(
        "courses/<int:course_id>/settings/",
        CourseSettingUpdateView.as_view(),
        name="course-setting",
    ),
]
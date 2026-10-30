from django.contrib import admin

from .models import Chapter, Course, CourseSetting, Question, Tag


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(CourseSetting)
class CourseSettingAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "target_accuracy",
        "review_interval",
        "created_at",
    )
    search_fields = ("course__name", "course__code")
    readonly_fields = ("created_at",)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("course", "name", "order", "created_at")
    list_filter = ("course",)
    search_fields = ("name", "course__name", "course__code")
    readonly_fields = ("created_at",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "created_at")
    search_fields = (
        "title",
        "content",
        "error_reason",
        "chapter__name",
        "chapter__course__name",
    )
    list_filter = ("chapter__course", "tags", "created_at")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at",)
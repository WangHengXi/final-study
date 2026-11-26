from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="課程名稱",
    )
    code = models.CharField(
        max_length=12,
        verbose_name="課程代碼",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_courses",
        verbose_name="課程建立者",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )

    class Meta:
        verbose_name = "課程"
        verbose_name_plural = "課程"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "code"],
                name="unique_course_code_per_owner",
            ),
        ]

    def __str__(self):
        return self.name


class StudyTask(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_tasks",
        verbose_name="安排者",
    )
    scheduled_date = models.DateField(verbose_name="安排日期")
    title = models.CharField(max_length=120, verbose_name="讀書事項")
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="study_tasks",
        verbose_name="關聯課程",
    )
    notes = models.TextField(blank=True, verbose_name="備註")
    is_completed = models.BooleanField(default=False, verbose_name="已完成")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "讀書事項"
        verbose_name_plural = "讀書事項"
        ordering = ("scheduled_date", "is_completed", "created_at")

    def __str__(self):
        return self.title


class CourseSetting(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name="learning_setting",
        verbose_name="課程",
    )
    target_accuracy = models.PositiveSmallIntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="目標正確率（%）",
    )
    review_interval = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1)],
        verbose_name="複習間隔（天）",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )

    class Meta:
        verbose_name = "課程學習設定"
        verbose_name_plural = "課程學習設定"

    def __str__(self):
        return f"{self.course.name}的學習設定"

class Chapter(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="所屬課程",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="章節名稱",
    )
    order = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="章節順序",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )

    class Meta:
        verbose_name = "章節"
        verbose_name_plural = "章節"
        ordering = ("order", "created_at")

    def __str__(self):
        return f"{self.course.name}｜{self.name}"

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="標籤名稱",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )

    class Meta:
        verbose_name = "錯題標籤"
        verbose_name_plural = "錯題標籤"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Question(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="所屬章節",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="題目名稱",
    )
    content = models.TextField(
        blank=True,
        verbose_name="題目內容",
    )
    error_reason = models.TextField(
        blank=True,
        verbose_name="錯誤原因",
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="questions",
        blank=True,
        verbose_name="錯題標籤",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )

    class Meta:
        verbose_name = "錯題"
        verbose_name_plural = "錯題"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

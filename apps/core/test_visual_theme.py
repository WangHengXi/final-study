from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.accounts.models import UserProfile
from apps.learning.models import Chapter, Course


class MorandiVisualThemeTests(SimpleTestCase):
    def test_shared_theme_exposes_the_morandi_purple_and_white_palette(self):
        theme_path = finders.find("core/studytrack-theme.css")

        self.assertIsNotNone(theme_path)
        theme_source = Path(theme_path).read_text(encoding="utf-8")

        for declaration in (
            "--page-bg: #faf9fc;",
            "--surface: #ffffff;",
            "--surface-subtle: #eeeaf2;",
            "--primary: #766782;",
            "--text: #403849;",
            "--text-muted: #6f6678;",
            "--border: #ddd5e4;",
            "--focus: #766782;",
        ):
            with self.subTest(declaration=declaration):
                self.assertIn(declaration, theme_source)

    def test_public_surface_sources_do_not_restore_retired_decorative_colors(self):
        source_paths = (
            settings.BASE_DIR / "apps/core/static/core/studytrack-theme.css",
            settings.BASE_DIR / "apps/core/static/core/navbar.css",
            settings.BASE_DIR / "static/final-study/css/home.css",
            settings.BASE_DIR / "static/final-study/css/study-calendar.css",
            settings.BASE_DIR / "apps/core/templates/core/home.html",
        )
        retired_colors = (
            "#ead1d7",
            "#dfbec7",
            "#dfbcc6",
            "#f0f3f0",
            "#f0e7eb",
            "#e7ece9",
        )

        for source_path in source_paths:
            source = source_path.read_text(encoding="utf-8").lower()
            for retired_color in retired_colors:
                with self.subTest(source=source_path.name, color=retired_color):
                    self.assertNotIn(retired_color, source)

    def test_course_sources_do_not_restore_retired_decorative_colors(self):
        source_paths = (
            settings.BASE_DIR / "apps/learning/templates/learning/course_form.html",
            settings.BASE_DIR / "apps/learning/templates/learning/course_list.html",
            settings.BASE_DIR / "apps/learning/templates/learning/course_detail.html",
            settings.BASE_DIR / "apps/learning/templates/learning/course_setting_form.html",
            settings.BASE_DIR / "apps/learning/templates/learning/question_form.html",
        )
        retired_colors = (
            "#ead1d7",
            "#dfbec7",
            "#dfbcc6",
            "#f0f3f0",
            "#f0e7eb",
            "#e7ece9",
        )

        for source_path in source_paths:
            source = source_path.read_text(encoding="utf-8").lower()
            for retired_color in retired_colors:
                with self.subTest(source=source_path.name, color=retired_color):
                    self.assertNotIn(retired_color, source)

    def test_course_validation_alerts_do_not_use_decorative_color_surfaces(self):
        source_paths = (
            settings.BASE_DIR / "apps/learning/templates/learning/course_form.html",
            settings.BASE_DIR / "apps/learning/templates/learning/course_detail.html",
        )

        for source_path in source_paths:
            source = source_path.read_text(encoding="utf-8")
            with self.subTest(source=source_path.name):
                self.assertNotIn("bg-red-50", source)
                self.assertNotIn("text-red-700", source)
                self.assertIn("theme-error", source)


class MorandiVisualThemePageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="visual-theme-user",
            password="test-password",
        )
        UserProfile.objects.create(user=self.user, display_name="視覺測試")
        self.course = Course.objects.create(
            owner=self.user,
            name="視覺測試課程",
            code="VISUAL101",
        )
        self.chapter = Chapter.objects.create(
            course=self.course,
            name="第一章",
            order=1,
        )

    def test_supported_pages_load_the_shared_visual_theme(self):
        responses = [self.client.get(reverse("core:home"))]
        self.client.force_login(self.user)
        responses.extend(
            (
                self.client.get(reverse("core:overview")),
                self.client.get(reverse("learning:study-calendar")),
                self.client.get(reverse("learning:course-list")),
                self.client.get(reverse("learning:course-create")),
                self.client.get(
                    reverse("learning:course-detail", args=[self.course.id])
                ),
                self.client.get(
                    reverse("learning:course-setting", args=[self.course.id])
                ),
                self.client.get(
                    reverse("learning:question-create", args=[self.chapter.id])
                ),
            )
        )

        for response in responses:
            with self.subTest(path=response.request["PATH_INFO"]):
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    f'href="{static("core/studytrack-theme.css")}"',
                )

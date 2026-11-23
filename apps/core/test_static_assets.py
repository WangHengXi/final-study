from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.accounts.models import UserProfile
from apps.learning.models import Chapter, Course


class FinalStudyStaticConfigurationTests(SimpleTestCase):
    def test_project_static_directory_and_js_placeholder_are_discoverable(self):
        self.assertIn(settings.BASE_DIR / "static", settings.STATICFILES_DIRS)
        self.assertIsNotNone(finders.find("final-study/js/.gitkeep"))


class FinalStudyHomeAssetTests(TestCase):
    def test_home_uses_external_stylesheet_without_inline_style(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(
            response,
            f'href="{static("final-study/css/home.css")}"',
        )
        self.assertNotContains(response, "<style>")


class FinalStudyLearningAssetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="asset-test-user",
            password="test-password",
        )
        UserProfile.objects.create(user=self.user, display_name="資產測試使用者")
        self.course = Course.objects.create(
            name="資產測試課程",
            code="ASSET101",
            owner=self.user,
        )
        self.chapter = Chapter.objects.create(
            course=self.course,
            name="第一章",
            order=1,
        )
        self.client.force_login(self.user)

    def test_learning_pages_use_external_stylesheets_without_inline_style(self):
        pages = {
            "course-list.css": self.client.get(reverse("learning:course-list")),
            "course-detail.css": self.client.get(
                reverse("learning:course-detail", args=[self.course.id])
            ),
            "question-form.css": self.client.get(
                reverse("learning:question-create", args=[self.chapter.id])
            ),
            "course-setting-form.css": self.client.get(
                reverse("learning:course-setting", args=[self.course.id])
            ),
        }

        for stylesheet, response in pages.items():
            with self.subTest(stylesheet=stylesheet):
                self.assertContains(
                    response,
                    f'href="{static(f"final-study/css/{stylesheet}")}"',
                )
                self.assertNotContains(response, "<style>")
                self.assertContains(response, "https://cdn.tailwindcss.com")

    def test_learning_stylesheets_are_discoverable(self):
        for stylesheet in (
            "course-list.css",
            "course-detail.css",
            "question-form.css",
            "course-setting-form.css",
        ):
            with self.subTest(stylesheet=stylesheet):
                self.assertIsNotNone(
                    finders.find(f"final-study/css/{stylesheet}")
                )


class FinalStudyAccountAssetTests(TestCase):
    def test_account_pages_share_external_stylesheet_and_keep_forms(self):
        user = get_user_model().objects.create_user(
            username="account-asset-test-user",
            password="test-password",
        )
        pages = {
            "login": ("account_login", self.client.get(reverse("account_login"))),
            "signup": ("account_signup", self.client.get(reverse("account_signup"))),
        }
        self.client.force_login(user)
        pages["logout"] = (
            "account_logout",
            self.client.get(reverse("account_logout")),
        )

        for name, (url_name, response) in pages.items():
            with self.subTest(page=name):
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    f'href="{static("final-study/css/account.css")}"',
                )
                self.assertNotContains(response, "<style>")
                self.assertContains(response, f'action="{reverse(url_name)}"')
                self.assertContains(response, 'name="csrfmiddlewaretoken"')
                self.assertContains(response, "https://cdn.tailwindcss.com")

    def test_account_stylesheet_is_discoverable(self):
        self.assertIsNotNone(finders.find("final-study/css/account.css"))

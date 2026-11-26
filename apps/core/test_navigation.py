from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse


class SharedNavigationTests(TestCase):
    def test_guest_account_page_has_shared_navigation(self):
        response = self.client.get(reverse("account_login"))

        self.assertContains(response, 'data-testid="shared-navbar"')
        self.assertContains(response, f'href="{reverse("core:home")}"')
        self.assertContains(response, f'href="{reverse("account_login")}"')
        self.assertContains(response, f'href="{reverse("account_signup")}"')

    def test_authenticated_user_without_profile_has_safe_navigation(self):
        user = get_user_model().objects.create_user(
            username="no-profile-user",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("learning:course-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="shared-navbar"')
        self.assertContains(response, f'href="{reverse("core:home")}"')
        self.assertContains(response, "備考 Overview")
        self.assertContains(response, "複習分析（即將推出）")
        self.assertContains(response, f'href="{reverse("core:overview")}"')
        self.assertContains(response, f'href="{reverse("learning:study-calendar")}"')
        self.assertContains(response, f'href="{reverse("learning:course-list")}"')
        self.assertContains(
            response,
            f'action="{reverse("account_logout")}"',
        )
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_shared_navigation_stylesheet_is_discoverable(self):
        self.assertIsNotNone(finders.find("core/navbar.css"))

    def test_home_uses_shared_shell_without_default_navigation(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(
            response,
            f'href="{static("core/navbar.css")}"',
        )
        self.assertContains(response, "把散落的備考，")
        self.assertNotContains(response, 'data-testid="shared-navbar"')
        self.assertNotContains(response, "https://cdn.tailwindcss.com")

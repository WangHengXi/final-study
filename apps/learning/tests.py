from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Course


class CourseDataViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="course-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="test-password",
        )
        self.url = reverse("learning:course-data")

    def create_course(self, *, owner=None, name="Mathematics", code="MATH"):
        return Course.objects.create(
            owner=owner or self.user,
            name=name,
            code=code,
        )

    def test_returns_only_the_requesting_users_filtered_second_page(self):
        for index in range(11):
            self.create_course(
                name=f"Mathematics {index}",
                code=f"M{index:03}",
            )
        self.create_course(
            owner=self.other_user,
            name="Mathematics private",
            code="PRIVATE",
        )
        self.create_course(name="History", code="HIST")

        self.client.force_login(self.user)
        response = self.client.get(
            self.url,
            {"q": "  mathematics  ", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["page"], 2)
        self.assertEqual(payload["page_size"], 10)
        self.assertEqual(payload["total_count"], 11)
        self.assertEqual(payload["total_pages"], 2)
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual(payload["items"][0]["name"], "Mathematics 0")
        self.assertNotIn("Mathematics private", {item["name"] for item in payload["items"]})
        self.assertEqual(
            payload["items"][0]["detail_url"],
            reverse("learning:course-detail", args=[payload["items"][0]["id"]]),
        )

    def test_rejects_invalid_page_as_json(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url, {"page": "not-a-page"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["error"], "invalid_page")

    def test_returns_json_401_to_anonymous_requests(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["error"], "authentication_required")


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "course-list-cache-tests",
        },
    },
)
class CourseListCacheTests(CourseDataViewTests):
    def setUp(self):
        super().setUp()
        cache.clear()

    def test_reuses_a_cached_payload_for_the_same_user_query_and_page(self):
        self.create_course(name="Mathematics", code="MATH101")
        self.client.force_login(self.user)

        first_response = self.client.get(self.url, {"q": "math", "page": 1})

        self.assertEqual(first_response.status_code, 200)
        with patch(
            "apps.learning.views.Course.objects.filter",
            side_effect=AssertionError("second request queried Course"),
        ):
            second_response = self.client.get(
                self.url,
                {"q": "math", "page": 1},
            )

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.json(), first_response.json())

    def test_keeps_cached_results_isolated_by_user_and_search(self):
        self.create_course(name="Mathematics", code="MATH101")
        Course.objects.create(
            owner=self.other_user,
            name="English",
            code="ENG101",
        )

        self.client.force_login(self.user)
        mathematics_response = self.client.get(self.url, {"q": "math"})
        english_for_first_user = self.client.get(self.url, {"q": "english"})

        self.client.force_login(self.other_user)
        english_for_second_user = self.client.get(self.url, {"q": "english"})

        self.assertEqual(
            [item["name"] for item in mathematics_response.json()["items"]],
            ["Mathematics"],
        )
        self.assertEqual(english_for_first_user.json()["items"], [])
        self.assertEqual(
            [item["name"] for item in english_for_second_user.json()["items"]],
            ["English"],
        )

    def test_creation_invalidates_only_the_creators_cached_list(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).json()["items"], [])

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(self.url).json()["items"], [])

        self.client.force_login(self.user)
        create_response = self.client.post(
            reverse("learning:course-create"),
            {"name": "Calculus", "code": "MATH101"},
        )
        refreshed_response = self.client.get(self.url)

        self.assertEqual(create_response.status_code, 302)
        self.assertEqual(
            [item["name"] for item in refreshed_response.json()["items"]],
            ["Calculus"],
        )

        self.client.force_login(self.other_user)
        with patch(
            "apps.learning.views.Course.objects.filter",
            side_effect=AssertionError("other user cache was invalidated"),
        ):
            other_response = self.client.get(self.url)

        self.assertEqual(other_response.json()["items"], [])

    def test_returns_course_data_when_cache_read_fails(self):
        self.create_course(name="Calculus", code="MATH101")
        self.client.force_login(self.user)

        with patch(
            "apps.learning.course_list_cache.cache.get",
            side_effect=ConnectionError("cache unavailable"),
        ):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["name"] for item in response.json()["items"]],
            ["Calculus"],
        )
        self.assertNotIn("cache unavailable", response.content.decode())

    def test_returns_course_data_when_cache_write_fails(self):
        self.create_course(name="Calculus", code="MATH101")
        self.client.force_login(self.user)

        with patch(
            "apps.learning.course_list_cache.cache.set",
            side_effect=ConnectionError("cache unavailable"),
        ):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["name"] for item in response.json()["items"]],
            ["Calculus"],
        )
        self.assertNotIn("cache unavailable", response.content.decode())

    def test_failed_creation_keeps_the_existing_cache_version(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).json()["items"], [])

        failed_creation = self.client.post(
            reverse("learning:course-create"),
            {"name": "Calculus", "code": ""},
        )

        self.assertEqual(failed_creation.status_code, 400)
        with patch(
            "apps.learning.views.Course.objects.filter",
            side_effect=AssertionError("failed creation invalidated cache"),
        ):
            response = self.client.get(self.url)

        self.assertEqual(response.json()["items"], [])


@override_settings(
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class CourseListPageTests(TestCase):
    def test_page_provides_an_ajax_shell_without_server_rendered_courses(self):
        user = get_user_model().objects.create_user(
            username="course-owner",
            password="test-password",
        )
        Course.objects.create(
            owner=user,
            name="Server rendered course",
            code="SERVER",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("learning:course-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-course-data-url="/learning/courses/data/"')
        self.assertContains(response, "/static/final-study/js/course-list.js")
        self.assertContains(response, 'aria-busy="true"')
        self.assertContains(response, "正在載入課程")
        self.assertContains(response, 'id="course-list-error"')
        self.assertNotContains(response, "Server rendered course")

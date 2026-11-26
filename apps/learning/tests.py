from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from . import models as learning_models
from .models import Course


class StudyTaskModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="study-task-owner",
            password="test-password",
        )

    def test_allows_multiple_tasks_on_the_same_day_with_safe_defaults(self):
        self.assertTrue(hasattr(learning_models, "StudyTask"))
        study_task = learning_models.StudyTask

        first = study_task.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="閱讀第二章",
        )
        second = study_task.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="整理錯題",
        )

        self.assertFalse(first.is_completed)
        self.assertIsNone(first.course)
        self.assertEqual(first.notes, "")
        self.assertEqual(
            list(study_task.objects.filter(owner=self.user)),
            [first, second],
        )

    def test_keeps_tasks_owned_by_their_creators(self):
        other_user = get_user_model().objects.create_user(
            username="other-study-task-owner",
            password="test-password",
        )
        self.assertTrue(hasattr(learning_models, "StudyTask"))
        study_task = learning_models.StudyTask

        own_task = study_task.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="自己的安排",
        )
        study_task.objects.create(
            owner=other_user,
            scheduled_date=date(2026, 12, 8),
            title="他人的安排",
        )

        self.assertEqual(
            list(study_task.objects.filter(owner=self.user)),
            [own_task],
        )


class StudyTaskFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="study-form-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="study-form-other",
            password="test-password",
        )
        self.owned_course = Course.objects.create(
            owner=self.user,
            name="專業課",
            code="MAJOR101",
        )
        self.other_course = Course.objects.create(
            owner=self.other_user,
            name="他人的課程",
            code="OTHER101",
        )

    def test_form_exposes_only_the_owners_courses(self):
        from . import forms as learning_forms

        self.assertTrue(hasattr(learning_forms, "StudyTaskForm"))
        form = learning_forms.StudyTaskForm(owner=self.user)

        self.assertEqual(
            list(form.fields["course"].queryset),
            [self.owned_course],
        )
        self.assertEqual(
            list(form.fields),
            ["scheduled_date", "title", "course", "notes"],
        )

    def test_form_rejects_another_users_course_and_preserves_bound_values(self):
        from . import forms as learning_forms

        self.assertTrue(hasattr(learning_forms, "StudyTaskForm"))
        form = learning_forms.StudyTaskForm(
            data={
                "scheduled_date": "2026-12-08",
                "title": "閱讀第二章",
                "course": self.other_course.id,
                "notes": "保留這段備註",
            },
            owner=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("course", form.errors)
        self.assertEqual(form.data["title"], "閱讀第二章")
        self.assertEqual(form.data["notes"], "保留這段備註")

    def test_form_rejects_blank_and_overlength_titles(self):
        from . import forms as learning_forms

        self.assertTrue(hasattr(learning_forms, "StudyTaskForm"))
        for title in ("", "x" * 121):
            with self.subTest(title=title):
                form = learning_forms.StudyTaskForm(
                    data={
                        "scheduled_date": "2026-12-08",
                        "title": title,
                    },
                    owner=self.user,
                )

                self.assertFalse(form.is_valid())
                self.assertIn("title", form.errors)

    def test_form_requires_an_owner(self):
        from . import forms as learning_forms

        self.assertTrue(hasattr(learning_forms, "StudyTaskForm"))
        with self.assertRaises(TypeError):
            learning_forms.StudyTaskForm()


class StudyCalendarViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="calendar-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="calendar-other-user",
            password="test-password",
        )
        self.url = reverse("learning:study-calendar")

    def test_month_shows_only_the_requesting_users_tasks_and_adjacent_months(self):
        study_task = learning_models.StudyTask
        study_task.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="閱讀第二章",
        )
        study_task.objects.create(
            owner=self.other_user,
            scheduled_date=date(2026, 12, 8),
            title="他人的安排",
        )
        self.client.force_login(self.user)

        response = self.client.get(self.url, {"month": "2026-12"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "閱讀第二章")
        self.assertNotContains(response, "他人的安排")
        self.assertContains(response, f"{self.url}?month=2026-11")
        self.assertContains(response, f"{self.url}?month=2027-01")

    def test_invalid_month_renders_the_current_month(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url, {"month": "not-a-month"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["display_month"], date.today().replace(day=1))

    def test_calendar_requires_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response["Location"])


class StudyTaskCrudViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="task-crud-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="task-crud-other",
            password="test-password",
        )
        self.course = Course.objects.create(
            owner=self.user,
            name="專業課",
            code="MAJOR201",
        )
        self.other_course = Course.objects.create(
            owner=self.other_user,
            name="其他人的專業課",
            code="OTHER201",
        )
        self.create_url = reverse("learning:study-task-create")

    def test_create_task_for_owned_course_redirects_to_its_month(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.create_url,
            {
                "scheduled_date": "2026-12-08",
                "title": "閱讀第二章",
                "course": self.course.id,
                "notes": "先整理觀念",
            },
        )

        self.assertRedirects(
            response,
            f"{reverse('learning:study-calendar')}?month=2026-12",
        )
        task = learning_models.StudyTask.objects.get(title="閱讀第二章")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.course, self.course)

    def test_invalid_foreign_course_does_not_create_a_task(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.create_url,
            {
                "scheduled_date": "2026-12-08",
                "title": "閱讀第二章",
                "course": self.other_course.id,
                "notes": "保留備註",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(learning_models.StudyTask.objects.count(), 0)
        self.assertIn("course", response.context["form"].errors)
        self.assertContains(response, "閱讀第二章", status_code=400)
        self.assertContains(response, "保留備註", status_code=400)

    def test_owner_can_edit_task_but_another_user_gets_404(self):
        task = learning_models.StudyTask.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="舊標題",
        )
        edit_url = reverse("learning:study-task-edit", args=[task.id])

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(edit_url).status_code, 404)

        self.client.force_login(self.user)
        response = self.client.post(
            edit_url,
            {
                "scheduled_date": "2026-11-04",
                "title": "新標題",
                "course": "",
                "notes": "改過的備註",
            },
        )

        self.assertRedirects(
            response,
            f"{reverse('learning:study-calendar')}?month=2026-11",
        )
        task.refresh_from_db()
        self.assertEqual(task.title, "新標題")
        self.assertEqual(task.notes, "改過的備註")


class StudyTaskActionViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="task-action-owner",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="task-action-other",
            password="test-password",
        )
        self.task = learning_models.StudyTask.objects.create(
            owner=self.user,
            scheduled_date=date(2026, 12, 8),
            title="閱讀第二章",
        )
        self.toggle_url = reverse("learning:study-task-toggle", args=[self.task.id])
        self.delete_url = reverse("learning:study-task-delete", args=[self.task.id])

    def test_owner_can_toggle_and_delete_a_task_with_post_requests(self):
        self.client.force_login(self.user)

        self.assertEqual(self.client.get(self.toggle_url).status_code, 405)
        toggle_response = self.client.post(self.toggle_url)
        self.assertRedirects(
            toggle_response,
            f"{reverse('learning:study-calendar')}?month=2026-12",
        )
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

        delete_response = self.client.post(self.delete_url)
        self.assertRedirects(
            delete_response,
            f"{reverse('learning:study-calendar')}?month=2026-12",
        )
        self.assertFalse(learning_models.StudyTask.objects.filter(id=self.task.id).exists())

    def test_other_user_cannot_toggle_or_delete_a_task(self):
        self.client.force_login(self.other_user)

        self.assertEqual(self.client.post(self.toggle_url).status_code, 404)
        self.assertEqual(self.client.post(self.delete_url).status_code, 404)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)


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

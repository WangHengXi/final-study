from html.parser import HTMLParser
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.learning.models import StudyTask


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append(("".join(self._text).strip(), self._href))
            self._href = None
            self._text = []


class HomePageTests(TestCase):
    def test_default_login_redirect_targets_the_study_dashboard(self):
        self.assertEqual(settings.LOGIN_REDIRECT_URL, "core:overview")

    def test_guest_sees_the_public_homepage(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "A LITTLE PLACE TO LEARN")
        self.assertContains(response, "備考英語")
        self.assertContains(response, "個人讀書安排")
        self.assertNotContains(response, "二次函數")
        self.assertNotContains(response, "小小提醒")
        self.assertNotContains(response, "今天的備考")

    def test_authenticated_user_still_sees_the_public_homepage(self):
        user = get_user_model().objects.create_user(
            username="home-test-user",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "A LITTLE PLACE TO LEARN")
        self.assertNotContains(response, "今天的備考")

    def test_dashboard_separates_only_the_users_tasks_for_today(self):
        user = get_user_model().objects.create_user(
            username="dashboard-owner",
            password="test-password",
        )
        other_user = get_user_model().objects.create_user(
            username="dashboard-other",
            password="test-password",
        )
        StudyTask.objects.create(
            owner=user,
            scheduled_date=date.today(),
            title="今天未完成的安排",
        )
        StudyTask.objects.create(
            owner=user,
            scheduled_date=date.today(),
            title="今天已完成的安排",
            is_completed=True,
        )
        StudyTask.objects.create(
            owner=other_user,
            scheduled_date=date.today(),
            title="其他使用者的安排",
        )
        StudyTask.objects.create(
            owner=user,
            scheduled_date=date(2026, 12, 8),
            title="不是今天的安排",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:overview"))

        self.assertContains(response, "今天未完成的安排")
        self.assertContains(response, "今天已完成的安排")
        self.assertContains(response, "未完成")
        self.assertContains(response, "已完成")
        self.assertContains(response, "新增今天的安排")
        self.assertContains(response, "查看行事曆")
        self.assertContains(response, "我的課程")
        self.assertNotContains(response, "其他使用者的安排")
        self.assertNotContains(response, "不是今天的安排")

    def test_dashboard_shows_an_empty_state_for_today(self):
        user = get_user_model().objects.create_user(
            username="dashboard-empty",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:overview"))

        self.assertContains(response, "今天還沒有安排")
        self.assertContains(response, "新增今天的安排")

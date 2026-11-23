from html.parser import HTMLParser

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
    def first_course_url(self, response):
        parser = AnchorParser()
        parser.feed(response.content.decode())
        return next(
            href
            for text, href in parser.links
            if text.startswith("建立我的第一門課")
        )

    def test_guest_first_course_action_links_to_login(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(self.first_course_url(response), reverse("account_login"))

    def test_authenticated_first_course_action_links_to_course_list(self):
        user = get_user_model().objects.create_user(
            username="home-test-user",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:home"))

        self.assertEqual(
            self.first_course_url(response),
            reverse("learning:course-list"),
        )

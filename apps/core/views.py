from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View

from apps.learning.models import StudyTask

class GoHomeView(View):
    def get(self, request):
        return redirect("core:home")


class TextResponseView(View):
    def get(self, request):
        return HttpResponse(
            "這是一份由 HttpResponse 回傳的純文字。",
            content_type="text/plain; charset=utf-8",
        )


class JsonResponseView(View):
    def get(self, request):
        return JsonResponse(
            {
                "message": "這是一份由 JsonResponse 回傳的資料。",
                "course": "Python 全端開發",
            },
            status=200,
        )

class HomeView(View):
    def get(self, request):
        return render(request, "core/home.html")


class OverviewView(LoginRequiredMixin, View):
    def get(self, request):
        today = timezone.localdate()
        today_tasks = StudyTask.objects.filter(
            owner=request.user,
            scheduled_date=today,
        ).select_related("course")
        return render(
            request,
            "core/dashboard.html",
            {
                "today": today,
                "incomplete_tasks": today_tasks.filter(is_completed=False),
                "completed_tasks": today_tasks.filter(is_completed=True),
            },
        )

class GreetingView(View):
    def get(self, request):
        name = request.GET.get("name", "訪客")
        context = {"name": name}
        return render(request, "core/greeting.html", context)



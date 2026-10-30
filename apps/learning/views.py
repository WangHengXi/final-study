from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Course


class CourseListView(View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        courses = Course.objects.select_related("owner")

        if keyword:
            courses = courses.filter(name__icontains=keyword)

        context = {
            "courses": courses,
            "keyword": keyword,
        }
        return render(request, "learning/course_list.html", context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = get_object_or_404(
            Course.objects.select_related(
                "learning_setting",
                "owner",
            ).prefetch_related(
                "chapters",
                "chapters__questions__tags",
            ),
            id=course_id,
        )

        return render(
            request,
            "learning/course_detail.html",
            {"course": course},
        )

class CourseCreateView(LoginRequiredMixin, View):
    template_name = "learning/course_form.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()

        context = {
            "name": name,
            "code": code,
        }

        if not name or not code:
            context["error"] = "請填寫課程名稱與課程代碼。"
            return render(
                request,
                self.template_name,
                context,
                status=400,
            )

        if len(name) > 100 or len(code) > 12:
            context["error"] = "課程名稱最多 100 字，課程代碼最多 12 字。"
            return render(
                request,
                self.template_name,
                context,
                status=400,
            )

        if Course.objects.filter(code=code).exists():
            context["error"] = "這個課程代碼已被使用，請改用其他代碼。"
            return render(
                request,
                self.template_name,
                context,
                status=400,
            )

        course = Course.objects.create(
            name=name,
            code=code,
            owner=request.user,
        )

        return redirect(
            "learning:course-detail",
            course_id=course.id,
        )
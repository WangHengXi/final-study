from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import Course


class CourseListView(View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        courses = Course.objects.all()

        if keyword:
            courses = courses.filter(name__icontains=keyword)

        context = {
            "courses": courses,
            "keyword": keyword,
        }
        return render(request, "learning/course_list.html", context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        return render(
            request,
            "learning/course_detail.html",
            {"course": course},
        )
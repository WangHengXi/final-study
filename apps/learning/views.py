from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from .course_list_cache import get_cached_course_payload, invalidate_course_list
from .models import Chapter, Course, CourseSetting
from .forms import CourseSettingForm, QuestionForm


class JsonLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse(
            {"error": "authentication_required"},
            status=401,
        )


class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()

        context = {
            "keyword": keyword,
        }

        return render(
            request,
            "learning/course_list.html",
            context,
        )


class CourseDataView(JsonLoginRequiredMixin, View):
    page_size = 10

    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        page_text = request.GET.get("page", "1")

        try:
            page_number = int(page_text)
        except (TypeError, ValueError):
            return JsonResponse({"error": "invalid_page"}, status=400)

        if page_number < 1:
            return JsonResponse({"error": "invalid_page"}, status=400)

        payload = get_cached_course_payload(
            user_id=request.user.id,
            keyword=keyword,
            page=page_number,
            loader=lambda: self.build_payload(
                request,
                keyword,
                page_number,
            ),
        )

        return JsonResponse(payload)

    def build_payload(self, request, keyword, page_number):
        courses = Course.objects.filter(
            owner=request.user,
        ).select_related("owner", "owner__profile")

        if keyword:
            courses = courses.filter(name__icontains=keyword)

        page = Paginator(courses, self.page_size).get_page(page_number)
        items = []
        for course in page.object_list:
            profile = getattr(course.owner, "profile", None)
            owner_display_name = (
                profile.display_name
                if profile and profile.display_name
                else course.owner.username
            )
            items.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "code": course.code,
                    "owner_display_name": owner_display_name,
                    "detail_url": reverse(
                        "learning:course-detail",
                        args=[course.id],
                    ),
                }
            )

        return {
            "items": items,
            "page": page.number,
            "page_size": self.page_size,
            "total_count": page.paginator.count,
            "total_pages": page.paginator.num_pages,
        }


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(
            Course.objects.select_related(
                "learning_setting",
                "owner",
                "owner__profile",
            ).prefetch_related(
                "chapters",
                "chapters__questions__tags",
            ),
            id=course_id,
            owner=request.user,
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

        if Course.objects.filter(
            owner=request.user,
            code=code,
        ).exists():
            context["error"] = "你的課程中已經有這個代碼，請改用其他代碼。"
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
        invalidate_course_list(request.user.id)

        return redirect(
            "learning:course-detail",
            course_id=course.id,
        )

class ChapterCreateView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        # 只能在自己建立的課程中新增章節
        course = get_object_or_404(
            Course,
            id=course_id,
            owner=request.user,
        )

        name = request.POST.get("name", "").strip()
        order_text = request.POST.get("order", "").strip()

        error = ""

        if not name:
            error = "請填寫章節名稱。"
        elif len(name) > 100:
            error = "章節名稱最多 100 個字元。"

        try:
            order = int(order_text)
            if not 1 <= order <= 32767:
                error = error or "章節順序請填寫 1～32767 的整數。"
        except ValueError:
            order = None
            error = error or "章節順序請填寫整數。"

        if error:
            return render(
                request,
                "learning/course_detail.html",
                {
                    "course": course,
                    "chapter_error": error,
                    "chapter_name": name,
                    "chapter_order": order_text,
                },
                status=400,
            )

        Chapter.objects.create(
            course=course,
            name=name,
            order=order,
        )

        return redirect(
            "learning:course-detail",
            course_id=course.id,
        )

class QuestionCreateView(LoginRequiredMixin, View):
    template_name = "learning/question_form.html"

    def get_chapter(self, request, chapter_id):
        return get_object_or_404(
            Chapter.objects.select_related("course"),
            id=chapter_id,
            course__owner=request.user,
        )

    def get(self, request, chapter_id):
        chapter = self.get_chapter(request, chapter_id)

        return render(
            request,
            self.template_name,
            {
                "chapter": chapter,
                "form": QuestionForm(),
            },
        )

    def post(self, request, chapter_id):
        chapter = self.get_chapter(request, chapter_id)
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.chapter = chapter
            question.save()
            form.save_m2m()

            return redirect(
                "learning:course-detail",
                course_id=chapter.course_id,
            )

        return render(
            request,
            self.template_name,
            {
                "chapter": chapter,
                "form": form,
            },
            status=400,
        )
class CourseSettingUpdateView(LoginRequiredMixin, View):
    template_name = "learning/course_setting_form.html"

    def get_course(self, request, course_id):
        return get_object_or_404(
            Course,
            id=course_id,
            owner=request.user,
        )

    def get(self, request, course_id):
        course = self.get_course(request, course_id)
        setting = CourseSetting.objects.filter(course=course).first()

        form = CourseSettingForm(instance=setting)

        return render(
            request,
            self.template_name,
            {
                "course": course,
                "form": form,
            },
        )

    def post(self, request, course_id):
        course = self.get_course(request, course_id)
        setting = CourseSetting.objects.filter(course=course).first()

        form = CourseSettingForm(
            request.POST,
            instance=setting,
        )

        if form.is_valid():
            CourseSetting.objects.update_or_create(
                course=course,
                defaults={
                    "target_accuracy": form.cleaned_data["target_accuracy"],
                    "review_interval": form.cleaned_data["review_interval"],
                },
            )

            return redirect(
                "learning:course-detail",
                course_id=course.id,
            )

        return render(
            request,
            self.template_name,
            {
                "course": course,
                "form": form,
            },
            status=400,
        )

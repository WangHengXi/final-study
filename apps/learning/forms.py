from django import forms

from .models import CourseSetting, Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content", "error_reason", "tags"]

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "例如：絕對誤差損失與中位數"}
            ),
            "content": forms.Textarea(attrs={"rows": 5}),
            "error_reason": forms.Textarea(attrs={"rows": 4}),
            "tags": forms.CheckboxSelectMultiple(),
        }

        help_texts = {
            "tags": "選填，可以選擇多個標籤。",
        }
class CourseSettingForm(forms.ModelForm):
    target_accuracy = forms.IntegerField(
        label="目標正確率（%）",
        min_value=0,
        max_value=100,
        initial=80,
        help_text="請輸入 0～100。",
    )
    review_interval = forms.IntegerField(
        label="複習間隔（天）",
        min_value=1,
        max_value=32767,
        initial=3,
        help_text="例如填寫 3，代表預計每 3 天複習一次。",
    )

    class Meta:
        model = CourseSetting
        fields = ["target_accuracy", "review_interval"]
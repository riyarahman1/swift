from django import forms
from swift.models import Topic, Subject, Course


class TopicForm(forms.ModelForm):
    name = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        error_messages={"required": "The name should not be empty"},
    )
    course = forms.ModelChoiceField(
        label="Course",
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Course.objects.filter(is_active=True),
        required=True,
    )
    subject = forms.ModelChoiceField(
        label="Subject",
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Subject.objects.none(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.data.get("course"):
            course_id = self.data.get("course")
            self.fields["subject"].queryset = Subject.objects.filter(
                course__id=course_id, is_active=True
            )
        elif self.instance.pk and self.instance.subject:
            course_id = self.instance.subject.course_id
            self.fields["subject"].queryset = Subject.objects.filter(
                course__id=course_id, is_active=True
            )

    class Meta:
        model = Topic
        fields = ["name", "course", "subject"]

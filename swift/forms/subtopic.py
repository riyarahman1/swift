from django import forms
from swift.models import Topic, Subject, Course, SubTopic


class SubTopicForm(forms.ModelForm):
    name = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        error_messages={"required": "The name should not be empty"},
    )
    topic = forms.ModelChoiceField(
        label="Topic",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_topic"}),
        queryset=Topic.objects.all(),
        required=True,
    )
    subject = forms.ModelChoiceField(
        label="Subject",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_subject"}),
        queryset=Subject.objects.none(),
        required=True,
    )
    course = forms.ModelChoiceField(
        label="Course",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_course"}),
        queryset=Course.objects.none(),
        required=True,
    )
    lessons = forms.CharField(
        label="Lessons",
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={"autocomplete": "off"}),
        error_messages={"required": "The lessons should not be empty"},
    )
    objectives = forms.CharField(
        label="Objectives",
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={"autocomplete": "off"}),
        error_messages={"required": "The objectives should not be empty"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.data.get("subject"):
            subject_id = self.data.get("subject")
            print("Subject ID:", subject_id)
            subject_ids = Subject.objects.filter(id=subject_id).values_list("id", flat=True)
            print("Subject IDs:", subject_ids)
            self.fields["subject"].queryset = Subject.objects.filter(id__in=subject_ids)
        elif self.instance.pk and self.instance.topic:
            topic_id = self.instance.topic_id
            subject_ids = Subject.objects.filter(topic__id=topic_id).values_list("id", flat=True)
            self.fields["subject"].queryset = Subject.objects.filter(id__in=subject_ids)
        else:
            self.fields["subject"].queryset = Subject.objects.none()

        if self.is_bound and self.data.get("subject"):
            subject_id = self.data.get("subject")
            print("Subject ID:", subject_id)
            course_ids = Course.objects.filter(course_subjects__id=subject_id).values_list("id", flat=True)
            self.fields["course"].queryset = Course.objects.filter(id__in=course_ids)
            print("Course IDs:", course_ids)

        elif self.instance.pk and self.instance.subject:
            subject_id = self.instance.subject_id
            course_ids = Course.objects.filter(
                course_subjects__id=subject_id).values_list("id", flat=True)
            self.fields["course"].queryset = Course.objects.filter(id__in=course_ids)
        else:
            self.fields["course"].queryset = Course.objects.none()

    class Meta:
        model = SubTopic
        fields = ["name", "topic", "subject", "course", "lessons", "objectives"]

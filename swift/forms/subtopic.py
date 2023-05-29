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
        widget=forms.Select(attrs={"class": "form-control", "id": "topic-select"}),
        queryset=Topic.objects.all(),
        required=True,
    )
    subject = forms.ModelChoiceField(
        label="Subject",
        widget=forms.Select(attrs={"class": "form-control", "id": "subject-select"}),
        queryset=Subject.objects.none(),
        required=True,
    )
    course = forms.ModelChoiceField(
        label="Course",
        widget=forms.Select(attrs={"class": "form-control", "id": "course-select"}),
        queryset=Course.objects.none(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound and self.data.get("topic"):
            topic_id = self.data.get("topic")
            self.fields["subject"].queryset = Subject.objects.filter(
                topic__id=topic_id
            )
        elif self.instance.pk and self.instance.topic:
            topic_id = self.instance.topic_id
            self.fields["subject"].queryset = Subject.objects.filter(
                topic__id=topic_id
            )
        if self.is_bound and self.data.get("subject"):
            subject_id = self.data.get("subject")
            self.fields["course"].queryset = Course.objects.filter(
                subject__id=subject_id
            )
        elif self.instance.pk and self.instance.subject:
            subject_id = self.instance.subject_id
            self.fields["course"].queryset = Course.objects.filter(
                subject__id=subject_id
            )

    class Meta:
        model = SubTopic
        fields = ["name", "topic", "subject", "course"]

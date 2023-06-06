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
        queryset=Topic.objects.none(),
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
        queryset=Course.objects.filter(is_active=True),
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
        super(SubTopicForm, self).__init__(*args, **kwargs)
        self.fields["topic"].queryset = Topic.objects.none()
        self.fields["subject"].queryset = Subject.objects.none()

        if "course" in self.data:
            try:
                course_id = int(self.data.get("course"))
                self.fields["subject"].queryset = Subject.objects.filter(
                    course_id=course_id
                )
            except (ValueError, TypeError):
                pass  
            
        if "subject" in self.data:
            try:
                subject_id = int(self.data.get("subject"))
                self.fields["topic"].queryset = Topic.objects.filter(
                    subject_id=subject_id
                )
            except (ValueError, TypeError):
                pass

    class Meta:
        model = SubTopic
        fields = ["name", "topic", "subject", "course", "lessons", "objectives"]

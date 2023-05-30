from django import forms
from swift.models import Topic, Subject, Course, SubTopic


# class SubTopicForm(forms.ModelForm):
#     name = forms.CharField(
#         label="Title",
#         max_length=200,
#         required=True,
#         widget=forms.TextInput(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The name should not be empty"},
#     )
#     topic = forms.ModelChoiceField(
#         label="Topic",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_topic"}),
#         queryset=Topic.objects.all(),
#         required=True,
#     )
#     subject = forms.ModelChoiceField(
#         label="Subject",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_subject"}),
#         queryset=Subject.objects.none(),
#         required=True,
#     )
#     course = forms.ModelChoiceField(
#         label="Course",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_course"}),
#         queryset=Course.objects.none(),
#         required=True,
#     )
#     lessons = forms.CharField(
#         label="Lessons",
#         max_length=100,
#         required=True,
#         widget=forms.Textarea(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The lessons should not be empty"},
#     )
#     objectives = forms.CharField(
#         label="Objectives",
#         max_length=100,
#         required=True,
#         widget=forms.Textarea(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The objectives should not be empty"},
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.is_bound and self.data.get("topic"):
#             topic_id = self.data.get("topic")
#             self.fields["subject"].queryset = Subject.objects.filter(topic_id=topic_id)
#         elif self.instance.pk and self.instance.topic:
#             topic_id = self.instance.topic_id
#             self.fields["subject"].queryset = Subject.objects.filter(topic_id=topic_id)
#         else:
#             self.fields["subject"].queryset = Subject.objects.none()

#         if self.is_bound and self.data.get("subject"):
#             subject_id = self.data.get("subject")
#             self.fields["course"].queryset = Course.objects.filter(subject_id=subject_id)
#         elif self.instance.pk and self.instance.subject:
#             subject_id = self.instance.subject_id
#             self.fields["course"].queryset = Course.objects.filter(subject_id=subject_id)
#         else:
#             self.fields["course"].queryset = Course.objects.none()

#     class Meta:
#         model = SubTopic
#         fields = ["name", "topic", "subject", "course", "lessons", "objectives"]

# class SubTopicForm(forms.ModelForm):
#     name = forms.CharField(
#         label="Title",
#         max_length=200,
#         required=True,
#         widget=forms.TextInput(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The name should not be empty"},
#     )
#     topic = forms.ModelChoiceField(
#         label="Topic",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_topic"}),
#         queryset=Topic.objects.all(),
#         required=True,
#     )
#     subject = forms.ModelChoiceField(
#         label="Subject",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_subject"}),
#         queryset=Subject.objects.none(),
#         required=True,
#     )
#     course = forms.ModelChoiceField(
#         label="Course",
#         widget=forms.Select(attrs={"class": "form-control", "id": "id_course"}),
#         queryset=Course.objects.none(),
#         required=True,
#     )
#     lessons = forms.CharField(
#         label="Lessons",
#         max_length=100,
#         required=True,
#         widget=forms.Textarea(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The lessons should not be empty"},
#     )
#     objectives = forms.CharField(
#         label="Objectives",
#         max_length=100,
#         required=True,
#         widget=forms.Textarea(attrs={"autocomplete": "off"}),
#         error_messages={"required": "The objectives should not be empty"},
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.is_bound and self.data.get("topic"):
#             topic_id = self.data.get("topic")
#             self.fields["subject"].queryset = Subject.objects.filter(topic_id=topic_id)
#         elif self.instance.pk and self.instance.topic:
#             topic_id = self.instance.topic_id
#             self.fields["subject"].queryset = Subject.objects.filter(topic_id=topic_id)
#         else:
#             self.fields["subject"].queryset = Subject.objects.none()

#         if self.is_bound and self.data.get("subject"):
#             subject_id = self.data.get("subject")
#             self.fields["course"].queryset = Course.objects.filter(subject_id=subject_id)
#         elif self.instance.pk and self.instance.subject:
#             subject_id = self.instance.subject_id
#             self.fields["course"].queryset = Course.objects.filter(subject_id=subject_id)
#         else:
#             self.fields["course"].queryset = Course.objects.none()

#         # Clear subject and course fields if topic is not selected
#         if not self.is_bound or not self.data.get("topic"):
#             self.fields["subject"].initial = None
#             self.fields["course"].initial = None

#     class Meta:
#         model = SubTopic
#         fields = ["name", "topic", "subject", "course", "lessons", "objectives"]


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
        if self.is_bound and self.data.get("topic"):
            topic_id = self.data.get("topic")
            self.fields["subject"].queryset = Subject.objects.filter(topic=topic_id)
        elif self.instance.pk and self.instance.topic:
            topic_id = self.instance.topic_id
            self.fields["subject"].queryset = Subject.objects.filter(topic=topic_id)
        else:
            self.fields["subject"].queryset = Subject.objects.none()

        if self.is_bound and self.data.get("subject"):
            subject_id = self.data.get("subject")
            self.fields["course"].queryset = Course.objects.filter(subject=subject_id)
        elif self.instance.pk and self.instance.subject:
            subject_id = self.instance.subject_id
            self.fields["course"].queryset = Course.objects.filter(subject=subject_id)
        else:
            self.fields["course"].queryset = Course.objects.none()

        # Clear subject and course fields if topic is not selected
        if not self.is_bound or not self.data.get("topic"):
            self.fields["subject"].initial = None
            self.fields["course"].initial = None

    class Meta:
        model = SubTopic
        fields = ["name", "topic", "subject", "course", "lessons", "objectives"]

from django import forms
from swift.models import Course, Curriculum


class CourseForm(forms.ModelForm):
    curriculum = forms.ModelChoiceField(
        label="Curriculum",
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Curriculum.objects.filter(is_active=True),
        required=True,
    )
    name = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        error_messages={"required": "The name should not be empty"},
    )

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields["curriculum"].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.country})"

    class Meta:
        model = Course
        fields = ["name", "curriculum"]

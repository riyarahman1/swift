from django import forms
from django.contrib.auth import authenticate
from swift.models import Curriculum


class CurriculumForm(forms.ModelForm):
    COUNTRY_CHOICES = [("", "---------")] + Curriculum.COUNTRY_CHOICES

    country = forms.ChoiceField(
        label="Country",
        choices=COUNTRY_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={"required": "The Country should not be empty"},
    )
    name = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
        error_messages={"required": "The name should not be empty"},
    )

    class Meta:
        model = Curriculum
        fields = ["name", "country"]

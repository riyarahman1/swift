from django import forms
from swift.models import Course, Curriculum

class CourseForm(forms.ModelForm):
    name = forms.CharField(
        label="Title",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        error_messages={'required': 'The name should not be empty'}
    )
    
    curriculum = forms.ModelChoiceField(
        label="curriculum",widget=forms.Select(attrs={'class':'form-control'}),
        queryset=Curriculum.objects.all(),
        required=True
    )

    class Meta:
        model = Course
        fields = ['name', 'curriculum']
        
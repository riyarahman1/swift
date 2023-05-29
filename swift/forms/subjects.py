from django import forms

from swift.models import Subject,Course

class SubjectsForm(forms.ModelForm):
    name = forms.CharField( 
        label="Title", max_length=200, required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The name should not be empty' }
    )
    course = forms.ModelChoiceField(
        label="course",widget=forms.Select(attrs={'class':'form-control'}),
        queryset=Course.objects.all(),
        required=True
    )
    
    
    class Meta:
        model = Subject
        fields = ['name','course']
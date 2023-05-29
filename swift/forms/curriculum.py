from django import forms
from django.contrib.auth import authenticate
from swift.models import Curriculum

class CurriculumForm(forms.ModelForm):
    name = forms.CharField( 
        label="Title", max_length=200, required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The name should not be empty' }
    )
    
    class Meta:
        model = Curriculum
        fields = ['name']
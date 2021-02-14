from django import forms
from django.forms.widgets import TextInput
from .models import Quiz
from django.forms import ModelForm

class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['dictionary', 'words_filter', 'length']

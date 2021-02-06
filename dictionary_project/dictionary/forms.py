from django import forms
from django.forms.widgets import TextInput
from .models import Dictionary

class CreateDictForm(forms.Form):
    lang_from = forms.CharField(label="Language From",max_length=100,
        widget=forms.TextInput(attrs={'class': "form-control dict-form"}))

    lang_to = forms.CharField(label='Language To',max_length=100,
        widget=forms.TextInput(attrs={'class': "form-control dict-form"}))

    color = forms.CharField(label='Color', max_length=7,
        widget=forms.TextInput(attrs={'type': 'color', 'class': "form-control dict-form color"}))

    
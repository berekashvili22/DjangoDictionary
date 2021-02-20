from django import forms
from django.forms.widgets import TextInput
from .models import Dictionary, Word

class CreateDictForm(forms.Form):
    LANGUAGE_CHOICES = (
        ('KA', 'GEORGIAN'),
        ('EN', 'ENGLISH'),
        ('RU', 'RUSSIAN'),
    )

    lang_from = forms.CharField(label="Language From",max_length=100,
        widget=forms.Select(choices=LANGUAGE_CHOICES, attrs={'class': "form-control dict-form"}))

    lang_to = forms.CharField(label='Language To',max_length=100,
        widget=forms.Select(choices=LANGUAGE_CHOICES, attrs={'class': "form-control dict-form"}))

    color = forms.CharField(label='Color', max_length=7,
        widget=forms.TextInput(attrs={'type': 'color', 'class': "form-control dict-form color"}))

    def __init__(self, *args, **kwargs):
        super(CreateDictForm, self).__init__(*args, **kwargs)
        # set select field's default values
        self.initial['lang_from'] = 'EN'
        self.initial['lang_to'] = 'KA'


class AddWordForm(forms.Form):
    original_word = forms.CharField(label="",max_length=45,
        widget=forms.TextInput(attrs={'class': "form-control word-form", 'placeholder': "ENTER WORD"}))

    translated_word = forms.CharField(label="",max_length=45,
        widget=forms.TextInput(attrs={'class': "form-control word-form", 'placeholder': "TRANSLATION"}))

    definition = forms.CharField(label="", required=False,
        widget=forms.TextInput(attrs={'class': "form-control word-form", 'placeholder': "DEFINITION"}, ))


class SearchWordForm(forms.Form):
     search_field = forms.CharField(label="",max_length=45,
        widget=forms.TextInput(attrs={'class': "form-control word-form search-input", 'placeholder': "ENTER WORD..."}))

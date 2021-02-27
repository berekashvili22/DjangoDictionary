from django import forms
from django.forms.widgets import TextInput
from .models import Quiz
from dictionary.models import Dictionary, Word
from django.forms import ModelForm


class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['dictionary', 'words_filter', 'length']

    def __init__(self, user, *args, **kwargs):
        super(CreateQuizForm, self).__init__(*args, **kwargs)
        self.fields['dictionary'].queryset = Dictionary.objects.filter(user=user)
        self.fields['dictionary'].empty_label = None
    
    

    def clean_dictionary(self):
        dictionary = self.cleaned_data.get('dictionary')
        # check dictionary words length
        words_count = Word.objects.filter(dictionary=dictionary).count()
        if words_count <= 0:
            raise forms.ValidationError("Dictionary is empty")
        return dictionary
    
    def clean_length(self):
        length = self.cleaned_data.get('length')
        dictionary = self.cleaned_data.get('dictionary')
        words_count = Word.objects.filter(dictionary=dictionary).count()
        if length > words_count:
            raise forms.ValidationError(f'Selected dictionary length is {words_count}, please pick number in that range') 
        return length
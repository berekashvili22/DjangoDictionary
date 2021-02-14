from django import forms
from django.forms.widgets import TextInput
from .models import Quiz
from django.forms import ModelForm

class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['dictionary', 'words_filter', 'length']




#     dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     RANDOM = 'RN'
#     NEW_WORDS = 'LA'
#     OLD_WORDS = 'OW'

#     WORDS_FILTER_CHOICES = (
#         (RANDOM, 'Random'),
#         (NEW_WORDS, 'New Words'),
#         (OLD_WORDS, 'Old Words'),
#     )

#     words_filter = models.CharField(max_length=255, verbose_name="Words Filter", choices=WORDS_FILTER_CHOICES)
#     length = models.IntegerField(default=20)
#     is_complete = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     dictionary = forms.CharField(label='Dictionary?', widget=forms.Select(choices=FRUIT_CHOICES))
from django.db import models
from django.contrib.auth.models import User

class Dictionary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_from = models.CharField(max_length=100, null=False)
    lang_to = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, default='fa5333')

    def __str__(self):
        return f'{self.lang_from} - {self.lang_to} dictionary'

class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    original_word = models.CharField(max_length=45, null=False)
    translated_word = models.CharField(max_length=45, null=False)
    description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.original_word}'


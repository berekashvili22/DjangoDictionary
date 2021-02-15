from django.db import models
from django.contrib.auth.models import User
from dictionary.models import *

# Create your models here.

class Quiz(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    RANDOM = 'RN'
    NEW_WORDS = 'LA'
    OLD_WORDS = 'OW'

    WORDS_FILTER_CHOICES = (
        (RANDOM, 'Random'),
        (NEW_WORDS, 'New Words'),
        (OLD_WORDS, 'Old Words'),
    )

    words_filter = models.CharField(max_length=255, verbose_name="Words Filter", choices=WORDS_FILTER_CHOICES, default=RANDOM)
    length = models.IntegerField(default=20)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.dictionary.lang_from} - {self.dictionary.lang_to} quiz {self.id}'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - quiz {self.quiz.id}'

    @property
    def answears(self):
        answears = Answear.objects.filter(question=self)
        return answears

class Answear(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - question {self.question.id}'

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(null=False)
    incorrect_words = models.TextField(null=False)
    correct_words = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)




     
from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz_home, name="quiz-home"),
    path('quiz/create/', views.quiz_form, name="quiz-form"),
    path('quiz/generate/', views.quiz_create, name="quiz-create"),
    path('quiz/live/<int:pk>', views.quiz, name="quiz"),
]
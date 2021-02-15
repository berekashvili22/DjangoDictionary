from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz_home, name="quiz-home"),
    path('quiz/add/', views.quiz_form, name="quiz-form"),
    path('quiz/live/', views.quiz_create, name="quiz-create"),
    path('quiz/write/<int:pk>', views.quiz, name="quiz"),
]
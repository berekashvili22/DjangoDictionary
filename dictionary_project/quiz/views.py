from django.shortcuts import render, redirect, HttpResponseRedirect
from . models import Quiz, Result, Question, Answear
from dictionary.models import Dictionary, Word
from . forms import CreateQuizForm
import json
from django.http import JsonResponse
from . utils import create_quiz, save_result, get_ids
from django.core.paginator import Paginator


def quiz_home(request):
    # get all words from dictionary
    result = Result.objects.filter(user=request.user).order_by('-date_created')
    # pagiante
    paginator = Paginator(result, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'results': result, 'page_obj': page_obj}
    return render(request, 'quiz/home.html', context)

def result(reqeuest, pk):
    result = Result.objects.get(pk=pk)
       
    correct_words_ids = get_ids(result.correct_words)
    incorrect_words_ids= get_ids(result.incorrect_words)

    correct_words = Word.objects.filter(id__in=correct_words_ids)
    incorrect_words = Word.objects.filter(id__in=incorrect_words_ids)

    context = {'result': result, 'correct_words': correct_words, 'incorrect_words': incorrect_words}
    return render(reqeuest, 'quiz/result.html', context)

def quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    context = {'questions': questions, 'quizId': quiz.id}
    return render(request, 'quiz/quiz.html', context)

def quiz_create(request):
    if request.method == "POST":
        form = CreateQuizForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            return create_quiz(data, user)
    else:
        form=CreateQuizForm(user=request.user)
    context = {'form': form}
    return render(request, 'quiz/quiz_form.html', context)


def result_save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        return save_result(data, user)
    else:
        return redirect('quiz')
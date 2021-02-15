from django.shortcuts import render, redirect, HttpResponseRedirect
from . models import Quiz, Result, Question, Answear
from dictionary.models import Dictionary, Word
from . forms import CreateQuizForm
import json
from django.http import JsonResponse
import random
from random_word import RandomWords


def quiz_home(request):
    # get all request.user dictionaries and order by date created
    # dictionaries = Dictionary.objects.all().filter(user=request.user).order_by('-date_created')
    context = {'quiz': 'quiz'}
    return render(request, 'quiz/home.html', context)

def quiz_form(request):
    form = CreateQuizForm()
    context = {'form': form}
    return render(request, 'quiz/quiz_form.html', context)

def quiz(request, pk):
    pk=32
    quiz = Quiz.objects.get(pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    answears = Answear.objects.filter(question__in=questions)
    context = {'questions': questions, 'answears': answears}
    return render(request, 'quiz/quiz.html', context)

def quiz_create(request):
    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            print('forma mivige')
            data = form.cleaned_data
            dictionary = data['dictionary']
            words_filter = data['words_filter']
            length = data['length']
            user = request.user

            r = RandomWords()
            
            print('rendomuli sitkvebis sia sheikmna')

            quiz = Quiz.objects.create(
                dictionary = dictionary,
                words_filter = words_filter,
                length = length,
                user = user,
            )

            quiz.save()

            print('quizi shevkmeni')
            
            words = ''

            if words_filter == 'RN':
                # create words ids list thats belongs to request dictionary
                valid_words_id_list = Word.objects.filter(dictionary=dictionary).values_list('id', flat=True)
                # create random id list in range of reqeust length (if reqeuest.length is > valid_words.length returns valid_words.length)
                random_words_id_list = random.sample(list(valid_words_id_list), min(len(valid_words_id_list), length))
                # get all words with id in random_words_id_list
                words = Word.objects.filter(id__in=random_words_id_list)

            print('cikli daiwko')
            for i in words:
                title = f'რა ნიშნავს სიტყვა - {i.translated_word} ?'
                question = Question.objects.create(
                    quiz= quiz,
                    title=title,
                )
                question.save()
                print('kitxva shevinaxe')

                correct_answear = i.original_word
                answears = [correct_answear]
                for i in range(3):
                    randomWord = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb")
                    if randomWord == None:
                        randomWord = 'test'
                    answears.append(randomWord)
                    print('pasuxebis sia gavanaxle axali rendom sitkvit')

                random.shuffle(answears)

                print('pasuxebis sia davashufle')

                for i in range(len(answears)):
                    is_true = True if correct_answear == answears[i] else False
                    print(answears[i])
                    print(i)
                    answear = Answear.objects.create(
                        question = question,
                        title = answears[i],
                        is_true = is_true,      
                    )
                    answear.save()

                    print('pasuxi shevinaxe')



    return HttpResponseRedirect('/quiz')
    

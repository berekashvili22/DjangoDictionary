from django.shortcuts import render, redirect, HttpResponseRedirect
from . models import Quiz, Result, Question, Answear
from dictionary.models import Dictionary, Word
from . forms import CreateQuizForm
import json
from django.http import JsonResponse
import random
from . words import getRandomWord


def quiz_home(request):
    results = Result.objects.all().filter(user=request.user).order_by('-date_created')
    context = {'results': results}
    return render(request, 'quiz/home.html', context)

def result(reqeuest, pk):
    result = Result.objects.get(pk=pk)
    def filterIds(l):
        l = l.replace("'", "")
        x = l.strip('][').split(', ') 
        y = []
        for i in x:
            y.append(int(i))
        return y
    correct_words_ids = filterIds(result.correct_words)
    incorrect_words_ids= filterIds(result.incorrect_words)

    correct_words = Word.objects.filter(id__in=correct_words_ids)
    incorrect_words = Word.objects.filter(id__in=incorrect_words_ids)

    # print(correct_words, incorrect_words)
    context = {'result': result, 'correct_words': correct_words, 'incorrect_words': incorrect_words}
    return render(reqeuest, 'quiz/result.html', context)

def quiz_form(request):
    form = CreateQuizForm()
    context = {'form': form}
    return render(request, 'quiz/quiz_form.html', context)

def quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    context = {'questions': questions, 'quizId': quiz.id}
    return render(request, 'quiz/quiz.html', context)

def quiz_create(request):
    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            # get form data
            data = form.cleaned_data
            dictionary = data['dictionary']
            words_filter = data['words_filter']
            length = data['length']
            user = request.user
            # create quiz with form data
            quiz = Quiz.objects.create(
                dictionary = dictionary,
                words_filter = words_filter,
                length = length,
                user = user,
            )
            quiz.save()
            # get words count of dictionary
            words_length = Word.objects.filter(dictionary=dictionary).count()
            # if form length>words_length use words_length
            max_length = min(words_length, length)
            # if words filter is set to random
            if words_filter == 'RN':
                # create words ids list thats belongs to request dictionary
                valid_words_id_list = Word.objects.filter(dictionary=dictionary).values_list('id', flat=True)
                # create random id list in range of reqeust length (if reqeuest.length is > valid_words.length returns valid_words.length)
                random_words_id_list = random.sample(list(valid_words_id_list), min(len(valid_words_id_list), length))
                # get all words with id in random_words_id_list
                words = Word.objects.filter(id__in=random_words_id_list)
            # if words filter is set to new words   
            if words_filter == "NW":
                # get last added words
                words = Word.objects.filter(dictionary=dictionary)[:max_length]
            # if words filter is set to old words
            if words_filter == "OW":
                # get oldest added words
                words = Word.objects.filter(dictionary=dictionary).order_by('-id')[:max_length]
            # create question for each words
            print(words)
            for word in words:
                # ტექსტი უნდა შევცვალო 
                title = f'რომელია {word.translated_word} - ის ინგლისური შესატყვისი ?'
                question = Question.objects.create(
                    id=word.id,
                    quiz=quiz,
                    title=title,
                )
                question.save()
                # set correct answear to question word's original_word
                correct_answear = word.original_word
                # list of answears
                answears = [correct_answear]
                # generate random words to update list of answears
                # ეს კიდე უნდა შევცვალო.... გენო დავიღალე
                for i in range(3):
                    # get random word 
                    randomWord = getRandomWord()
                    # just in case
                    if randomWord == None:
                        randomWord = 'test'
                    #  IQ LEVEL POSEIDON    
                    if randomWord == correct_answear:
                        randomWord = getRandomWord()
                    #update answears list with random word
                    answears.append(randomWord)
                
                # სწორი პასუხი სულ პირველი რომ არ იყოს
                random.shuffle(answears)

                #create question answears
                for i in range(len(answears)):
                    is_true = True if correct_answear == answears[i] else False
                    answear = Answear.objects.create(
                        question = question,
                        title = answears[i],
                        is_true = is_true,      
                    )
                    answear.save()

    return HttpResponseRedirect('/quiz/live/%s' % (quiz.id
    ))


def result_save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        quiz = Quiz.objects.get(id=data['quizId'])
        dictionary = quiz.dictionary
        correct = len(data['CorrectAnswears'])
        incorrect = len(data['IncorrectAnswears'])
        total = correct + incorrect   
        #  get x/100 score
        score = (correct * 100) // total
        Result.objects.create(
            dictionary = dictionary,
            user = request.user,
            score = score,
            correct_count = correct,
            incorrect_count = incorrect,
            correct_words = data['CorrectAnswears'],
            incorrect_words = data['IncorrectAnswears'] 
        )
        quiz.delete()
        return JsonResponse({"status": "success"})
    else:
        return redirect('quiz')
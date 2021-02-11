from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import CreateView
from . models import Dictionary, Word
from . forms import CreateDictForm, AddWordForm, SearchWordForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

def home(request):
    return render(request, 'dictionary/home.html')

@login_required
def dictionaries(request):
    # get all request.user dictionaries and order by date created
    dictionaries = Dictionary.objects.all().filter(user=request.user).order_by('-date_created')
    context = {'dictionaries': dictionaries}
    return render(request, 'dictionary/dictionaries.html', context)

@login_required
def dictionary(request, pk):
    # get dictionary by passed primary key
    dictionary = Dictionary.objects.get(pk=pk)
    form = AddWordForm()
    # form1 = SearchWordForm()  --- ???  
    if request.user == dictionary.user:
        # get all words from dictionary
        words = Word.objects.all().filter(dictionary=dictionary.id)
        # pagiante
        paginator = Paginator(words, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'dictionary': dictionary, 'form': form ,'page_obj': page_obj}
        if request.method == "POST":
            # update word
            form = AddWordForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Word.objects.create(
                    original_word = data['original_word'],
                    translated_word = data['translated_word'],
                    definition = data['definition'],
                    dictionary = dictionary,
                )
                # return last on last page of pagination
                return HttpResponseRedirect('/dictionary/%s?page=%s'  % (dictionary.id, paginator.num_pages))
    # if request user != dictionary.user return back to dictionaries page  
    else:
        return redirect('dictionaries')
    return render(request, 'dictionary/dictionary.html', context)

@login_required
def dictionary_create(request):
    # create dictionary from
    form = CreateDictForm
    context = {'form': form}
    return render(request, 'dictionary/dictionary_form.html', context)

@login_required
def dictionary_save(request):
    # if request method is POST validate data and create dictionary
    if request.method == "POST":
        form = CreateDictForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Dictionary.objects.create(
                lang_from = data['lang_from'],
                lang_to = data['lang_to'],
                color = data['color'],
                user = request.user,
            )
            return redirect('dictionaries')
    #  if request method is not POST do nothing
    else:
        pass
    return redirect('dictionaries')


@login_required
def dictionary_update(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # get updated word data
            data = json.loads(request.body)
            # get word id
            print(data)
            exit
            wordId = data['wordId']
            action = data['action']
            # get updated word
            word = Word.objects.get(pk=wordId)
            if word.dictionary.user == request.user:
                # check action type
                if action == "save":
                    # update word with new data
                    word.original_word = data['original']
                    word.translated_word = data['translated']
                    word.definition = data['definition']
                    word.save()
                if action == "delete":
                    word.delete()
            else:
                return redirect('home')

            return JsonResponse(
                {'originalWord': data['original'],
                'translatedWord': data['translated'],
                'definition': data['definition'],
                'wordId': data['wordId'],
                'action': data['action']},
                 safe=False)
    else:
        return redirect('home')

@login_required
def dictionary_filter(request):
    if request.method == 'POST':
        words = Word.filter(
            original_word__starts_with=searchOriginal) | Word.filter(
            translated_word__starts_with=searchTranslated) | Word.filter(
            definition_word__starts_with=searchDefinition)

        data = words.values()

        return JsonResponse(list(data), safe=False)
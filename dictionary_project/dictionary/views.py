from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import CreateView
from . models import Dictionary, Word
from . forms import CreateDictForm, AddWordForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
    if request.user == dictionary.user:
        # get all words from dictionary
        words = Word.objects.all().filter(dictionary=dictionary.id)
        # pagiante
        paginator = Paginator(words, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'dictionary': dictionary, 'form': form, 'page_obj': page_obj}
        if request.method == "POST":
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

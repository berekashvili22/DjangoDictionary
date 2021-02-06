from django.shortcuts import render, redirect
from django.views.generic import CreateView
from . models import Dictionary, Word
from . forms import CreateDictForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'dictionary/home.html')

@login_required
def dictionaries(request):
    dictionaries = Dictionary.objects.all().filter(user=request.user).order_by('-date_created')
    context = {'dictionaries': dictionaries}
    return render(request, 'dictionary/dictionaries.html', context)

@login_required
def dictionary(request, pk):
    dictionary = Dictionary.objects.get(pk=pk)
    if request.user == dictionary.user:
        words = Word.objects.all().filter(dictionary=dictionary.id)
        context = {'dictionary': dictionary, 'words': words}
    else:
        return redirect('dictionaries')
    return render(request, 'dictionary/dictionary.html', context)

@login_required
def dictionary_create(request):
    form = CreateDictForm
    context = {'form': form}
    return render(request, 'dictionary/dictionary_form.html', context)

@login_required
def dictionary_save(request):
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
    else:
        pass
    return redirect('dictionaries')
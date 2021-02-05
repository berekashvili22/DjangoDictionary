from django.shortcuts import render, redirect
from . models import Dictionary, Word

def home(request):
    return render(request, 'dictionary/home.html')

def dictionaries(request):
    dictionaries = Dictionary.objects.all().filter(user=request.user)
    context = {'dictionaries': dictionaries}
    return render(request, 'dictionary/dictionaries.html', context)

def dictionary(request):
    dictionary = Dictionary.objects.get(id=1)
    words = Word.objects.all().filter(dictionary=dictionary.id)
    context = {'dictionary': dictionary, 'words': words}
    return render(request, 'dictionary/dictionary.html', context)

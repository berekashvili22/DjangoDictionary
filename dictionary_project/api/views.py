from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import DictionarySerializer, WordSerializer

from quiz.models import Quiz, Result
from dictionary.models import Dictionary, Word 
from datetime import datetime, timedelta

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'task-list',
        'Detail View':'/task-detail/<str:pk>',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>',
        'Delete':'/task-delete/<str:pk>',
    }
    return Response(api_urls)

@api_view(['GET'])
def progressData(request):
    user = request.user
    dicts = Dictionary.objects.filter(user=user)
    words = Word.objects.filter(dictionary__in=dicts)
    dicts_count = dicts.count()
    words_count = words.count()
    quiz_count = Result.objects.filter(user=user).count()


    today = datetime.now()
    one_week_ago = datetime.today() - timedelta(days=7)

    words_this_year = words.filter(date_added__year=today.year).count()
    words_this_month = words.filter(date_added__year=today.year, date_added__month=today.month).count()
    words_this_week = words.filter(date_added__year=today.year, date_added__month=today.month, date_added__gte=one_week_ago).count()
    words_this_day = words.filter(date_added__year=today.year, date_added__month=today.month, date_added__day=today.day).count()

    data = {
        'dicts_count': dicts_count,
        'words_count': words_count,
        'quizes_count': quiz_count,
        'words_this_year': words_this_year,
        'words_this_month': words_this_month,
        'words_this_week': words_this_week,
        'words_this_day': words_this_day,
    }
    return Response(data)
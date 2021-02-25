from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . serializers import DictionarySerializer, WordSerializer

from quiz.models import Quiz, Result
from dictionary.models import Dictionary, Word 
from datetime import datetime, timedelta

from django.db.models import Avg, Count, Min, Sum, Max

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
@permission_classes([IsAuthenticated])
def progressData(request):
    user = request.user
    dicts = Dictionary.objects.filter(user=user)
    words = Word.objects.filter(dictionary__in=dicts)
    quizes = Result.objects.filter(user=user)

    dicts_count = dicts.count()
    words_count = words.count()
    quiz_count = quizes.count()


    today = datetime.now()
    one_week_ago = datetime.today() - timedelta(days=7)

    words_this_year = words.filter(date_added__year=today.year).count()
    words_this_month = words.filter(date_added__year=today.year, date_added__month=today.month).count()
    words_this_week = words.filter(date_added__year=today.year, date_added__month=today.month, date_added__gte=one_week_ago).count()
    words_this_day = words.filter(date_added__year=today.year, date_added__month=today.month, date_added__day=today.day).count()

    dicts_this_year = dicts.filter( date_created__year=today.year).count()
    dicts_this_month = dicts.filter( date_created__year=today.year,  date_created__month=today.month).count()
    dicts_this_week = dicts.filter( date_created__year=today.year,  date_created__month=today.month,  date_created__gte=one_week_ago).count()
    dicts_this_day = dicts.filter( date_created__year=today.year,  date_created__month=today.month,  date_created__day=today.day).count()

    quizes_this_year = quizes.filter( date_created__year=today.year).count()
    quizes_this_month = quizes.filter( date_created__year=today.year,  date_created__month=today.month).count()
    quizes_this_week = quizes.filter( date_created__year=today.year,  date_created__month=today.month,  date_created__gte=one_week_ago).count()
    quizes_this_day = quizes.filter( date_created__year=today.year,  date_created__month=today.month,  date_created__day=today.day).count()

    result = Result.objects.filter(user=user)
    total_score = result.aggregate(Sum('score'))
    average_score = result.aggregate(Avg('score'))
    min_score = result.aggregate(Min('score'))
    max_score = result.aggregate(Max('score'))

    correct = round(average_score['score__avg'])
    incorrect = 100 - correct

    #averge score by months
   
    avg_jan = round(result.filter(date_created__year=today.year, date_created__month=1).aggregate(Avg('score'))['score__avg'] or 0)
    avg_feb = round(result.filter(date_created__year=today.year, date_created__month=2).aggregate(Avg('score'))['score__avg'] or 0)
    avg_mar = round(result.filter(date_created__year=today.year, date_created__month=3).aggregate(Avg('score'))['score__avg'] or 0)
    avg_apr = round(result.filter(date_created__year=today.year, date_created__month=4).aggregate(Avg('score'))['score__avg'] or 0)
    avg_may = round(result.filter(date_created__year=today.year, date_created__month=5).aggregate(Avg('score'))['score__avg'] or 0)
    avg_jun = round(result.filter(date_created__year=today.year, date_created__month=6).aggregate(Avg('score'))['score__avg'] or 0)
    avg_jul = round(result.filter(date_created__year=today.year, date_created__month=7).aggregate(Avg('score'))['score__avg'] or 0)
    avg_aug = round(result.filter(date_created__year=today.year, date_created__month=8).aggregate(Avg('score'))['score__avg'] or 0)
    avg_sep = round(result.filter(date_created__year=today.year, date_created__month=9).aggregate(Avg('score'))['score__avg'] or 0)
    avg_oct = round(result.filter(date_created__year=today.year, date_created__month=10).aggregate(Avg('score'))['score__avg'] or 0)
    avg_nov = round(result.filter(date_created__year=today.year, date_created__month=11).aggregate(Avg('score'))['score__avg'] or 0)
    avg_dec = round(result.filter(date_created__year=today.year, date_created__month=12).aggregate(Avg('score'))['score__avg'] or 0)

    data = {
        'total': {
            'dicts': dicts_count,
            'words': words_count,
            'quizes': quiz_count,
        },
        'dateLabels': ['Year', 'Month', 'Week', 'Day'],
        'words_by_date': {
            'values': [words_this_year, words_this_month, words_this_week, words_this_day],
        },
        'dicts_by_date': {
            'values': [dicts_this_year, dicts_this_month, dicts_this_week, dicts_this_day],
        },
        'quizes_by_date': {
            'values': [quizes_this_year, quizes_this_month, quizes_this_week, quizes_this_day],
        },
        'quizScore':{
            'total': total_score['score__sum'],
            'averge': round(average_score['score__avg']),
            'min': min_score['score__min'],
            'max': max_score['score__max'],
            'quiz_count': quiz_count,
        },
        'successRate':{
            'correct': correct,
            'incorrect': incorrect,
        },
        'avgScoreByMonth':{
            'Jan.': avg_jan,
            'Feb.': avg_feb,
            'Mar.': avg_mar,
            'Apr.': avg_apr,
            'May': avg_may,
            'June': avg_jun,
            'July': avg_jul,
            'Aug.': avg_aug,
            'Sept.':avg_sep,
            'Oct.': avg_oct,
            'Nov.': avg_nov,
            'Dec.': avg_dec
        }
    }

    return Response(data)
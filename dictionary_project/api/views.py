from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . serializers import DictionarySerializer, WordSerializer


from . utils import chartData


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
    data = chartData(user)
    return Response(data)
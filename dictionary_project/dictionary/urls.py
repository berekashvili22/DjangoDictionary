from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dictionaries', views.dictionaries, name="dictionaries"),
    path('dictionary', views.dictionary, name="dictionary"),
]
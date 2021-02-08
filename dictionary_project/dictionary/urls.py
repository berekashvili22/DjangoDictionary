from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dictionaries', views.dictionaries, name="dictionaries"),
    path('dictionary/<int:pk>', views.dictionary, name="dictionary"),
    path('dictionary/new/', views.dictionary_create, name="dictionary_form"),
    path('dictionary/save/', views.dictionary_save, name="dictionary_save"),
    path('dictionary/update/', views.dictionary_update, name="dictionary_update"),
]
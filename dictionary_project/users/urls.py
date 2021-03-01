from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
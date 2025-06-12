from django.urls import path
from . import views

urlpatterns = [
    path('', views.controller_screen, name='controller_screen'),
]
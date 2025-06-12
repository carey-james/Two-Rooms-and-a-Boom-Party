from django.urls import path
from . import views

urlpatterns = [
    path('', views.controller_screen, name='controller_screen'), # Web interface
    path('api/timer/', views.get_timer, name='get_timer'),  # JSON API
]
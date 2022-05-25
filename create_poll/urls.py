from django.urls import path, include
from .views import create_poll

urlpatterns = [
    path('', create_poll)
]
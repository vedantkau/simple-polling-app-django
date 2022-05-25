from django.urls import path
from .views import respond_poll

urlpatterns = [
    path('', respond_poll)
]
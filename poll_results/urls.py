from django.urls import path
from .views import view_poll_result

urlpatterns = [
    path('', view_poll_result)
]
"""polling_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import subprocess
import sys

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('create_poll.urls')),
    path('results', include('poll_results.urls')),
    path('respond', include('respond_poll.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

poll_cleaner_script = None

def poll_cleaner():
    #Start poll_cleaner script to run in background
    global poll_cleaner_script
    project_base_dir = settings.BASE_DIR
    poll_cleaner_script = subprocess.Popen(["python", f"{project_base_dir}/poll_cleaner/poll_cleaner.py"], shell=True)

if sys.argv == ['manage.py', 'runserver']:
    poll_cleaner()

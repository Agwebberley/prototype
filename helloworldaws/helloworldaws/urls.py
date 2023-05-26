# This code is defining the URL patterns for a Django project. It imports the necessary modules from
# Django (`admin` and `path` from `django.contrib` and `django.urls`, respectively) and sets up the
# URL patterns using a list of `urlpatterns`.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CRUD.urls')),
]

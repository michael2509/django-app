from django.urls import path

from .views import libraries

urlpatterns = [
    path('libraries', libraries, name='libraries'),
]
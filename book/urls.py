from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('book/search', views.search, name='search'),
    path('libraries', views.libraries, name='libraries'),
]
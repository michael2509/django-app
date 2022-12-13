from django.urls import path
from .views import libraries

from . import views

urlpatterns = [
    # ex: /book/
    path('', views.index, name='index'),
    # ex: /book/5/
    path('<int:book_id>/', views.detail, name='detail'),
    # ex: /book/5/borrow/
    path('<int:book_id>/borrow/', views.borrow, name='borrow'),
    path('libraries', libraries, name='libraries'),
]
from django.urls import path
from . import views
from .views import AddBook

urlpatterns = [
    path('', views.index, name='index'),
    path('book/search', views.search, name='search'),
    path('libraries', views.libraries, name='libraries'),
    # Routes du Back Office
    path('back-office/add-book', AddBook.as_view(), name='add_book')
]
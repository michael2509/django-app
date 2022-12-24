from django.urls import path
from . import views
from .views import AddBook

urlpatterns = [
    path('', views.index, name='index'),
    path('book/search', views.search, name='search'),
    path('libraries', views.libraries, name='libraries'),
    # Routes du Back Office
    path('back-office/libraries', views.libraries_owned, name='libraries_owned'),
    path('back-office/libraries/<int:library_id>', views.library, name='library'),
    path('back-office/libraries/<int:library_id>/borrow-book', views.borrow_book, name='borrow_book'),
    path('back-office/add-book', AddBook.as_view(), name='add_book'),
]
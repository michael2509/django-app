from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('book/search', views.search, name='search'),
    path('libraries', views.libraries, name='libraries'),
    path('chat', views.chat, name='chat'),
    # Routes du Back Office
    path('back-office/libraries', views.libraries_owned, name='libraries_owned'),
    path('back-office/library/<int:library_id>', views.library, name='library'),
    path('back-office/library/<int:library_id>/add-book', views.add_book, name='add_book'),
    path('back-office/library/<int:library_id>/borrow-book', views.borrow_book, name='borrow_book'),
    path('back-office/library/<int:library_id>/late-borrow-list', views.late_borrow_list, name='late_borrow_list'),
    path('back-office/library/<int:library_id>/lecture-group', views.lecture_group, name='lecture_group'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
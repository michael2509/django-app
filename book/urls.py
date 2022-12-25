from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('book/search', views.search, name='search'),
    path('libraries', views.libraries, name='libraries'),
    # Routes du Back Office
    path('back-office/libraries', views.libraries_owned, name='libraries_owned'),
    path('back-office/libraries/<int:library_id>', views.library, name='library'),
    path('back-office/libraries/<int:library_id>/borrow-book', views.borrow_book, name='borrow_book'),
    path('back-office/libraries/<int:library_id>/add-book', views.add_book, name='add_book')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
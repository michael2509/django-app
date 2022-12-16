from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('book/', include('book.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('book/', include('book.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
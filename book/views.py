from django.shortcuts import render
from .models import Library

# Create your views here.
def index(request):
    libraries = Library.objects.all()
    context = {'libraries': libraries}
    return render(request, 'library/index.html', context)
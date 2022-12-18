from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Book, Library, Book_instance
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render


def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            messages.success(request, 'Success')
        else:  
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')


def index(request):
    book_list = get_list_or_404(Book) 

    context = {
        'book_list': book_list,
    }
    return render(request, 'book/index.html', context)


def libraries(request):
    if 'department_code' in request.GET:
        department_code = request.GET.get('department_code')
        libraries = Library.objects.filter(department_code=department_code)
        return render(request, 'library/index.html', {'libraries': libraries})

    else:
        libraries = Library.objects.all()
        return render(request, 'library/index.html', {'libraries': libraries})


def search(request):
    if 'book_name' in request.GET:
        book_name = request.GET.get('book_name')
        book_instances = Book_instance.objects.filter(book__title__icontains=book_name)

        return render(request, 'book/search.html', {'book_instances': book_instances})
    else:
        return render(request, 'book/search.html')
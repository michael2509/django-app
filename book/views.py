from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Book, Library, BookInstance
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import AddBookForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        book_instances = BookInstance.objects.filter(book__title__icontains=book_name)

        return render(request, 'book/search.html', {'book_instances': book_instances})
    else:
        return render(request, 'book/search.html')


class AddBook(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    form_class = AddBookForm
    success_url = reverse_lazy("add_book")
    template_name = "book/add_book.html"

    # allow this views only to users with role bookseller
    def test_func(self):
        print(self.request.user.role)
        return self.request.user.role == 'bookseller'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully')
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Error adding book')
            return render(request , self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request , self.template_name, {'form': form})
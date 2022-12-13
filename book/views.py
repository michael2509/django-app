from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Book, Library, Book_instance
from django.template import loader
from django.http import Http404

# Create your views here.

def index(request):
    # book_list = Book.objects.all()
    book_list = get_list_or_404(Book) 
    # Example for return directly the data
    # output = ', '.join([b.book_title for b in book_list])
    # return HttpResponse(output)
    
    # Good practice to return the data to the template
    context = {
        'book_list': book_list,
    }
    return render(request, 'book/index.html', context)
    # equivalent to
    # return HttpResponse(template.render(context, request))

def detail(request, book_id):
    # return HttpResponse("You're looking at book %s." % book_id)
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/detail.html', {'book': book})
    # same as
    # try:
    #     book = Book.objects.get(pk=book_id)
    # except Book.DoesNotExist:
    #     raise Http404("Book does not exist")
    # return render(request, 'book/detail.html', {'book': book})

def borrow(request, book_id):
    return HttpResponse("You're trying to borrow the book %s." % book_id)

# Create a function view to display all libraries
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
        
        # get book instances with the book name
        book_instances = Book_instance.objects.filter(book__title__icontains=book_name)

        # # get books from book_instances
        # books = [book_instance.book for book_instance in book_instances]

        return render(request, 'book/search.html', {'book_instances': book_instances})
    else:
        return render(request, 'book/search.html')


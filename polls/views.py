from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@permission_required('polls.view_question')
def customer(request):
    return HttpResponse("Routes for customers")


@permission_required('polls.delete_question')
def bookseller(request):
    return HttpResponse("Routes for booksellers")
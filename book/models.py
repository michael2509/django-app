from django.db import models
from accounts.models import User
from datetime import datetime, timedelta

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    genre = models.CharField(max_length=30)
    cover = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    borrow_date = models.DateField('date borrowed', null=True, blank=True)
    return_date = models.DateField('date returned', null=True, blank=True)

    def __str__(self):
        return "%s (bibliothèque : %s)" % (self.book, self.library)


class Library(models.Model):
    name = models.CharField(max_length=200, default="Bibliothèque sans nom")
    adress = models.CharField(max_length=200)
    department_code = models.IntegerField(default=75)
    owners = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class LectureGroup(models.Model):
    participants = models.ManyToManyField(User)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)    

    startDateTime = models.DateTimeField('start date time of the meeting', default=datetime.now())
    endDateTime = models.DateTimeField('start date time of the meeting', default=datetime.now() + timedelta(hours=1))


    def __str__(self):
        return "Groupe de lecture chez %s du %s à %s" % (self.library.name, self.startDateTime, self.endDateTime)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creationDateTime = models.DateTimeField('date of creation', default=datetime.now())

    def __str__(self):
        return "Message de %s envoyé le %s" % (self.sender.username, self.creationDateTime)
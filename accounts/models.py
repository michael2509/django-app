from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # create a role field that can be only 'customer' or 'bookseller'
    role = models.CharField(max_length=10, default='customer', choices=[('customer', 'customer'), ('bookseller', 'bookseller')])

    def __str__(self):
        return self.username
from __future__ import unicode_literals
from ..registration.models import Users
from django.db import models

class BooksManager(models.Manager):
    def registerbook(self, **kwargs):
        errors = False
        error_list = []
        if [required for required in ['title','author','rating','review'] if required in kwargs.keys()]:
            for key in kwargs.keys():
                if kwargs[key] == "":
                    errors = True
                    error_list.append("{} field missing!".format(key))
        else:
            errors = True
            error_list.append("Some fields were not passed to registerbook method.")
        if errors:
            return (True, error_list)
        else:
            return (False, "Review Added!")
        # return True if [required for required in ['title','author','rating','review'] if required in kwargs.keys()] else False

class Books(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BooksManager()

class Reviews(models.Model):
    rating = models.IntegerField()
    review = models.TextField()
    book = models.ForeignKey('Books', models.DO_NOTHING, related_name="bookid")
    user = models.ForeignKey(Users)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

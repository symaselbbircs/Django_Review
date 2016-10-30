from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from . import models
from ..registration.models import Users

# Create your views here.
def index(request):
    if 'uid' not in request.session:
        messages.error(request, "Please login to get to this page.")
        return redirect(reverse('login-main'))
    books = models.Reviews.objects.all().select_related().order_by('-updated_at')
    print [e.book.id for e in models.Reviews.objects.all().select_related().order_by('-updated_at')]
    if len(books) > 3:
        context = {'detailed_review': books[:3],
                   'other_reviews': books[3:]}
    elif len(books) <= 3:
        context = {'detailed_review': books}
    else:
        context = {}
    return render(request,
    'books/index.html', context)

def addreview(request, bookid):
    if request.method == "POST":
        print request.POST
        if len(request.POST['review']) >= 2:
            r = models.Reviews(rating = request.POST['rating'],
                               review=request.POST['review'],
                               book_id=bookid,
                               user_id=request.session['uid'])
            r.save()
    return redirect(reverse('books-show', kwargs={'bookid':bookid}))

def addbook(request):
    if request.method == "GET":
        authors = models.Books.objects.all().values('author').distinct()
        print authors
        if len(authors) >= 2:
            context = {'authors': authors}
        else:
            context = {}
        return render(request,
        'books/addbook.html', context)
    elif request.method == "POST":
        print request.POST
        title = request.POST['title']
        if request.POST['new_author']:
            author = request.POST['new_author']
        else:
            author = request.POST['old_author']
        review = request.POST['review']
        rating = request.POST['rating']
        errors =  models.Books.objects.registerbook(title = title, author = author, review = review, rating = rating)
        if errors[0]:
            for error in errors[1]:
                messages.error(request, error)
            return redirect(reverse('books-add'))
        else:
            b = models.Books(title = title, author = author)
            b.save()
            r = models.Reviews(review = review, rating = rating, book=b, user=Users.objects.get(id=request.session['uid']))
            r.save()
            return redirect(reverse('books-index'))

def read(request, bookid):
    book = models.Reviews.objects.filter(book__id = bookid).order_by('-updated_at')
    context = {'data': book}
    return render(request,
    'books/books.html', context)

def users(request, userid):
    user = Users.objects.filter(id=userid)
    print user
    reviews = models.Reviews.objects.filter(user__id=userid).annotate(Count('review'))
    context = {'reviews': reviews,
               'user': user}
    print reviews
    return render(request,
    'books/users.html', context)

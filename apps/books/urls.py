from django.conf.urls import url
from . import views as v

urlpatterns = [
    url(r'^$', v.index, name="books-index"),
    url(r'^add/$', v.addbook, name="books-add"),
    url(r'^(?P<bookid>\d*)/$', v.read, name="books-show"),
    url(r'^addreview/(?P<bookid>\d*)/$', v.addreview, name="books-addreview"),
    url(r'^u(?P<userid>\d*)/$', v.users, name="books-users")
]

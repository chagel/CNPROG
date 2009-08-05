import os.path
from django.conf.urls.defaults import *
from django.contrib import admin
from forum.views import index
from forum import views as app
from forum.feed import RssLastestQuestionsFeed

admin.autodiscover()
feeds = {
    'rss': RssLastestQuestionsFeed
}

APP_PATH = os.path.dirname(__file__)
urlpatterns = patterns('',
    (r'^$', index),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/content/images/favicon.ico'}),
    (r'^favicon\.gif$', 'django.views.generic.simple.redirect_to', {'url': '/content/images/favicon.gif'}),
    (r'^content/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(APP_PATH, 'templates/content').replace('\\','/')}
    ),
    (r'^upfiles/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(APP_PATH, 'templates/upfiles').replace('\\','/')}
    ),
    (r'^account/', include('django_authopenid.urls')),
    (r'^signin/$', 'django_authopenid.views.signin'),
    url(r'^about/$', app.about, name='about'),
    url(r'^faq/$', app.faq, name='faq'),
    url(r'^privacy/$', app.privacy, name='privacy'),
    url(r'^logout/$', app.logout, name='logout'),
    url(r'^answers/(?P<id>\d+)/comments/$', app.answer_comments, name='answer_comments'),
    url(r'^answers/(?P<id>\d+)/edit/$', app.edit_answer, name='edit_answer'),
    url(r'^answers/(?P<id>\d+)/revisions/$', app.answer_revisions, name='answer_revisions'),
    url(r'^questions/$', app.questions, name='questions'),
    url(r'^questions/ask/$', app.ask, name='ask'),
    url(r'^questions/unanswered/$', app.unanswered, name='unanswered'),
    url(r'^questions/(?P<id>\d+)/edit/$', app.edit_question, name='edit_question'),
    url(r'^questions/(?P<id>\d+)/close/$', app.close, name='close'),
    url(r'^questions/(?P<id>\d+)/reopen/$', app.reopen, name='reopen'),
    url(r'^questions/(?P<id>\d+)/answer/$', app.answer, name='answer'),
    url(r'^questions/(?P<id>\d+)/vote/$', app.vote, name='vote'),
    url(r'^questions/(?P<id>\d+)/revisions/$', app.question_revisions, name='question_revisions'),
    url(r'^questions/(?P<id>\d+)/comments/$', app.question_comments, name='question_comments'),
    url(r'^questions/(?P<question_id>\d+)/comments/(?P<comment_id>\d+)/delete/$', app.delete_question_comment, name='delete_question_comment'),
    url(r'^answers/(?P<answer_id>\d+)/comments/(?P<comment_id>\d+)/delete/$', app.delete_answer_comment, name='delete_answer_comment'),
    #place general question item in the end of other operations
    url(r'^questions/(?P<id>\d+)//*', app.question, name='question'),
    (r'^tags/$', app.tags),
    (r'^tags/(?P<tag>[^/]+)/$', app.tag),
    (r'^users/$',app.users),
    url(r'^users/(?P<id>\d+)/edit/$', app.edit_user, name='edit_user'),
    url(r'^users/(?P<id>\d+)//*', app.user, name='user'),
    url(r'^badges/$',app.badges, name='badges'),
    url(r'^badges/(?P<id>\d+)//*', app.badge, name='badge'),
    url(r'^messages/markread/$',app.read_message, name='read_message'),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^nimda/(.*)', admin.site.root),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^upload/$', app.upload),
    url(r'^books/$', app.books, name='books'),
    url(r'^books/ask/(?P<short_name>[^/]+)/$', app.ask_book, name='ask_book'),
    url(r'^books/(?P<short_name>[^/]+)/$', app.book, name='book'),
    url(r'^search/$', app.search, name='search'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

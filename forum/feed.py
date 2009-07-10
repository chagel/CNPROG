#!/usr/bin/env python
#encoding:utf-8
#-------------------------------------------------------------------------------
# Name:        Syndication feed class for subsribtion
# Purpose:
#
# Author:      Mike
#
# Created:     29/01/2009
# Copyright:   (c) CNPROG.COM 2009
# Licence:     GPL V2
#-------------------------------------------------------------------------------
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.utils.translation import ugettext as _
from models import Question
class RssLastestQuestionsFeed(Feed):
    title = _('site title') + _(' - ') + _('site slogan') + _(' - ')+ _('latest questions')
	#EDIT!!!
    link = 'http://where.com/questions/'
    description = _('meta site content')
    #ttl = 10
    copyright = _('copyright message')

    def item_link(self, item):
        return '/questions/%s/' % item.id

    def item_author_name(self, item):
        return item.author.username

    def item_author_link(self, item):
        return item.author.get_profile_url()

    def item_pubdate(self, item):
        return item.added_at

    def items(self, item):
       return Question.objects.filter(deleted=False).order_by('-added_at')[:30]

def main():
    pass

if __name__ == '__main__':
    main()

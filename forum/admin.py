# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class QuestionAdmin(admin.ModelAdmin):
    """Question admin class"""

class TagAdmin(admin.ModelAdmin):
    """Tag admin class"""

class Answerdmin(admin.ModelAdmin):
    """Answer admin class"""

class CommentAdmin(admin.ModelAdmin):
    """  admin class"""

class VoteAdmin(admin.ModelAdmin):
    """  admin class"""

class FlaggedItemAdmin(admin.ModelAdmin):
    """  admin class"""

class FavoriteQuestionAdmin(admin.ModelAdmin):
    """  admin class"""

class QuestionRevisionAdmin(admin.ModelAdmin):
    """  admin class"""

class AnswerRevisionAdmin(admin.ModelAdmin):
    """  admin class"""

class AwardAdmin(admin.ModelAdmin):
    """  admin class"""

class BadgeAdmin(admin.ModelAdmin):
    """  admin class"""

class ReputeAdmin(admin.ModelAdmin):
    """  admin class"""

class ActivityAdmin(admin.ModelAdmin):
    """  admin class"""
    
class BookAdmin(admin.ModelAdmin):
    """  admin class"""
    
class BookAuthorInfoAdmin(admin.ModelAdmin):
    """  admin class"""
    
class BookAuthorRssAdmin(admin.ModelAdmin):
    """  admin class"""    
    
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Answer, Answerdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(FlaggedItem, FlaggedItemAdmin)
admin.site.register(FavoriteQuestion, FavoriteQuestionAdmin)
admin.site.register(QuestionRevision, QuestionRevisionAdmin)
admin.site.register(AnswerRevision, AnswerRevisionAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Repute, ReputeAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthorInfo, BookAuthorInfoAdmin)
admin.site.register(BookAuthorRss, BookAuthorRssAdmin)
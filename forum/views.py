# encoding:utf-8
import calendar
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage
from django.core.paginator import InvalidPage
from django.core.paginator import Paginator
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.html import *
from django.utils.translation import ugettext as _
from markdown2 import Markdown
import os.path
import random
import time

import datetime
from forum import auth
from forum.auth import *
from forum.const import *
from forum.diff import textDiff as htmldiff
from forum.forms import *
from forum.models import *
from forum.user import *
from utils.html import sanitize_html

# used in index page
INDEX_PAGE_SIZE = 20
INDEX_AWARD_SIZE = 15
INDEX_TAGS_SIZE = 100
# used in tags list
DEFAULT_PAGE_SIZE = 60
# used in questions
QUESTIONS_PAGE_SIZE = 10
# used in users
USERS_PAGE_SIZE = 35
# used in answers
ANSWERS_PAGE_SIZE = 10
markdowner = Markdown(html4tags=True)
question_type = ContentType.objects.get_for_model(Question)
answer_type = ContentType.objects.get_for_model(Answer)
comment_type = ContentType.objects.get_for_model(Comment)
question_revision_type = ContentType.objects.get_for_model(QuestionRevision)
answer_revision_type = ContentType.objects.get_for_model(AnswerRevision)
repute_type = ContentType.objects.get_for_model(Repute)
question_type_id = question_type.id
answer_type_id = answer_type.id
comment_type_id = comment_type.id
question_revision_type_id = question_revision_type.id
answer_revision_type_id = answer_revision_type.id
repute_type_id = repute_type.id
def _get_tags_cache_json():
    tags = Tag.objects.filter(deleted=False).all()
    tags_list = []
    for tag in tags:
        dic = {'n': tag.name, 'c': tag.used_count}
        tags_list.append(dic)
    tags = simplejson.dumps(tags_list)
    return tags

def index(request):
    view_id = request.GET.get('sort', None)
    view_dic = {
        "latest":"-last_activity_at",
        "hottest":"-answer_count",
        "mostvoted":"-score",
        "trans": "-last_activity_at"
        }
    try:
        orderby = view_dic[view_id]
    except KeyError:
        view_id = "latest"
        orderby = "-last_activity_at"
    # group questions by author_id of 28,29
    if view_id == 'trans':
        questions = Question.objects.get_translation_questions(orderby, INDEX_PAGE_SIZE)
    else:
        questions = Question.objects.get_questions_by_pagesize(orderby, INDEX_PAGE_SIZE)
    # RISK - inner join queries
    questions = questions.select_related()
    tags = Tag.objects.get_valid_tags(INDEX_TAGS_SIZE)

    awards = Award.objects.get_recent_awards()

    return render_to_response('index.html', {
                              "questions": questions,
                              "tab_id": view_id,
                              "tags": tags,
                              "awards": awards[:INDEX_AWARD_SIZE],
                              }, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def faq(request):
    return render_to_response('faq.html', context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html', context_instance=RequestContext(request))

def unanswered(request):
    return questions(request, unanswered=True)

def questions(request, tagname=None, unanswered=False):
    """
    List of Questions, Tagged questions, and Unanswered questions.
    """
    # template file
    # "questions.html" or "unanswered.html"
    template_file = "questions.html"
    # get pagesize from session, if failed then get default value
    pagesize = request.session.get("pagesize", 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    view_id = request.GET.get('sort', None)
    view_dic = {"latest":"-added_at", "active":"-last_activity_at", "hottest":"-answer_count", "mostvoted":"-score"}
    try:
        orderby = view_dic[view_id]
    except KeyError:
        view_id = "latest"
        orderby = "-added_at"

    # check if request is from tagged questions
    if tagname is not None:
        objects = Question.objects.get_questions_by_tag(tagname, orderby)
    elif unanswered:
        #check if request is from unanswered questions
        template_file = "unanswered.html"
        objects = Question.objects.get_unanswered_questions(orderby)
    else:
        objects = Question.objects.get_questions(orderby)

    # RISK - inner join queries
    objects = objects.select_related(depth=1);
    objects_list = Paginator(objects, pagesize)
    questions = objects_list.page(page)

    # Get related tags from this page objects
    if questions.object_list.count() > 0:
        related_tags = Tag.objects.get_tags_by_questions(questions.object_list)
    else:
        related_tags = None
    return render_to_response(template_file, {
                              "questions": questions,
                              "tab_id": view_id,
                              "questions_count": objects_list.count,
                              "tags": related_tags,
                              "searchtag": tagname,
                              "is_unanswered": unanswered,
                              "context": {
                              'is_paginated': True,
                              'pages': objects_list.num_pages,
                              'page': page,
                              'has_previous': questions.has_previous(),
                              'has_next': questions.has_next(),
                              'previous': questions.previous_page_number(),
                              'next': questions.next_page_number(),
                              'base_url': request.path + '?sort=%s&' % view_id,
                              'pagesize': pagesize
                              }}, context_instance=RequestContext(request))

def create_new_answer(question=None, author=None, \
                      added_at=None, wiki=False, \
                      text='', email_notify=False):

    html = sanitize_html(markdowner.convert(text))

    #create answer
    answer = Answer(
                    question=question,
                    author=author,
                    added_at=added_at,
                    wiki=wiki,
                    html=html
                    )
    if answer.wiki:
        answer.last_edited_by = answer.author
        answer.last_edited_at = added_at 
        answer.wikified_at = added_at 

    answer.save()

    #update question data
    question.last_activity_at = added_at 
    question.last_activity_by = author 
    question.save()
    Question.objects.update_answer_count(question)

    #update revision
    AnswerRevision.objects.create(
                                  answer=answer,
                                  revision=1,
                                  author=author,
                                  revised_at=added_at,
                                  summary=CONST['default_version'],
                                  text=text
                                  )

    #set notification/delete
    if email_notify:
        try:
            EmailFeed.objects.get(feed_id=question.id, subscriber_id=author.id, feed_content_type=question_type)
        except EmailFeed.DoesNotExist:
            feed = EmailFeed(content=question, subscriber=author)
            feed.save()
    else:
        #not sure if this is necessary. ajax should take care of this...
        try:
            feed = Email.objects.get(feed_id=question.id, subscriber_id=author.id, feed_content_type=question_type)
            feed.delete()
        except:
            pass

def create_new_question(title=None, author=None, added_at=None,
                        wiki=False, tagnames=None, summary=None,
                        text=None):
    """this is not a view
    and maybe should become one of the methods on Question object?
    """
    html = sanitize_html(markdowner.convert(text))
    question = Question(
                        title=title,
                        author=author,
                        added_at=added_at,
                        last_activity_at=added_at,
                        last_activity_by=author,
                        wiki=wiki,
                        tagnames=tagnames,
                        html=html,
                        summary=summary
                        )
    if question.wiki:
        question.last_edited_by = question.author
        question.last_edited_at = added_at
        question.wikified_at = added_at

    question.save()

    # create the first revision
    QuestionRevision.objects.create(
                                    question=question,
                                    revision=1,
                                    title=question.title,
                                    author=author,
                                    revised_at=added_at,
                                    tagnames=question.tagnames,
                                    summary=CONST['default_version'],
                                    text=text
                                    )
    return question

#TODO: allow anynomus user to ask question by providing email and username.
#@login_required
def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():

            added_at = datetime.datetime.now()
            title = strip_tags(form.cleaned_data['title']).strip()
            wiki = form.cleaned_data['wiki']
            tagnames = form.cleaned_data['tags'].strip()
            text = form.cleaned_data['text']
            html = sanitize_html(markdowner.convert(text))
            summary = strip_tags(html)[:120]

            if request.user.is_authenticated():
                author = request.user 

                question = create_new_question(
                                               title=title,
                                               author=author,
                                               added_at=added_at,
                                               wiki=wiki,
                                               tagnames=tagnames,
                                               summary=summary,
                                               text=text
                                               )

                return HttpResponseRedirect(question.get_absolute_url())
            else:
                request.session.flush()
                session_key = request.session.session_key
                question = AnonymousQuestion(
                                             session_key=session_key,
                                             title=title,
                                             tagnames=tagnames,
                                             wiki=wiki,
                                             text=text,
                                             summary=summary,
                                             added_at=added_at,
                                             ip_addr=request.META['REMOTE_ADDR'],
                                             )
                question.save()
                return HttpResponseRedirect('%s%s%s' % (_('/account/'), _('signin/'), ('newquestion/')))
    else:
        form = AskForm()

    tags = _get_tags_cache_json()
    return render_to_response('ask.html', {
                              'form': form,
                              'tags': tags,
                              }, context_instance=RequestContext(request))

def question(request, id):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    view_id = request.GET.get('sort', 'votes')
    view_dic = {"latest":"-added_at", "oldest":"added_at", "votes":"-score"}
    try:
        orderby = view_dic[view_id]
    except KeyError:
        view_id = "votes"
        orderby = "-score"

    question = get_object_or_404(Question, id=id)
    if question.deleted and not can_view_deleted_post(request.user, question):
        raise Http404
    answer_form = AnswerForm(question, request.user)
    answers = Answer.objects.get_answers_from_question(question, request.user, orderby)
    answers = answers.select_related(depth=1)

    favorited = question.has_favorite_by_user(request.user)
    question_vote = question.votes.select_related().filter(user=request.user)
    if question_vote is not None and question_vote.count() > 0:
        question_vote = question_vote[0]

    user_answer_votes = {}
    for vote in question.get_user_votes_in_answers(request.user):
        if not user_answer_votes.has_key(vote.object_id):
            vote_value = -1
            if vote.is_upvote():
                vote_value = 1
            user_answer_votes[vote.object_id] = vote_value      
    
    filtered_answers = []
    for answer in answers:
        if answer.deleted == True:
            if answer.author_id == request.user.id:
                filtered_answers.append(answer)
        else:
            filtered_answers.append(answer)

    objects_list = Paginator(filtered_answers, ANSWERS_PAGE_SIZE)
    page_objects = objects_list.page(page)
    # update view count
    Question.objects.update_view_count(question)
    return render_to_response('question.html', {
                              "question": question,
                              "question_vote": question_vote,
                              "question_comment_count":question.comments.count(),
                              "answer": answer_form,
                              "answers": page_objects.object_list,
                              "user_answer_votes": user_answer_votes,
                              "tags": question.tags.all(),
                              "tab_id": view_id,
                              "favorited": favorited,
                              "similar_questions": Question.objects.get_similar_questions(question),
                              "context": {
                              'is_paginated': True,
                              'pages': objects_list.num_pages,
                              'page': page,
                              'has_previous': page_objects.has_previous(),
                              'has_next': page_objects.has_next(),
                              'previous': page_objects.previous_page_number(),
                              'next': page_objects.next_page_number(),
                              'base_url': request.path + '?sort=%s&' % view_id,
                              'extend_url': "#sort-top"
                              }
                              }, context_instance=RequestContext(request))

@login_required
def close(request, id):
    question = get_object_or_404(Question, id=id)
    if not can_close_question(request.user, question):
        return HttpResponse('Permission denied.')
    if request.method == 'POST':
        form = CloseForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            question.closed = True
            question.closed_by = request.user
            question.closed_at = datetime.datetime.now()
            question.close_reason = reason
            question.save()
        return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = CloseForm()
        return render_to_response('close.html', {
                                  'form': form,
                                  'question': question,
                                  }, context_instance=RequestContext(request))

@login_required
def reopen(request, id):
    question = get_object_or_404(Question, id=id)
    # open question
    if not can_reopen_question(request.user, question):
        return HttpResponse('Permission denied.')
    if request.method == 'POST':
        Question.objects.filter(id=question.id).update(closed=False,
                                                       closed_by=None, closed_at=None, close_reason=None)
        return HttpResponseRedirect(question.get_absolute_url())
    else:
        return render_to_response('reopen.html', {
                                  'question': question,
                                  }, context_instance=RequestContext(request))

@login_required
def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    if question.deleted and not can_view_deleted_post(request.user, question):
        raise Http404
    if can_edit_post(request.user, question):
        return _edit_question(request, question)
    elif can_retag_questions(request.user):
        return _retag_question(request, question)
    else:
        raise Http404

def _retag_question(request, question):
    if request.method == 'POST':
        form = RetagQuestionForm(question, request.POST)
        if form.is_valid():
            if form.has_changed():
                latest_revision = question.get_latest_revision()
                retagged_at = datetime.datetime.now()
                # Update the Question itself
                Question.objects.filter(id=question.id).update(
                                                               tagnames=form.cleaned_data['tags'],
                                                               last_edited_at=retagged_at,
                                                               last_edited_by=request.user,
                                                               last_activity_at=retagged_at,
                                                               last_activity_by=request.user
                                                               )
                # Update the Question's tag associations
                tags_updated = Question.objects.update_tags(question,
                                                            form.cleaned_data['tags'], request.user)
                # Create a new revision
                QuestionRevision.objects.create(
                                                question=question,
                                                title=latest_revision.title,
                                                author=request.user,
                                                revised_at=retagged_at,
                                                tagnames=form.cleaned_data['tags'],
                                                summary=CONST['retagged'],
                                                text=latest_revision.text
                                                )
                # send tags updated singal
                tags_updated.send(sender=question.__class__, question=question)

            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = RetagQuestionForm(question)
    return render_to_response('question_retag.html', {
                              'question': question,
                              'form': form,
                              'tags': _get_tags_cache_json(),
                              }, context_instance=RequestContext(request))


def _edit_question(request, question):
    latest_revision = question.get_latest_revision()
    revision_form = None
    if request.method == 'POST':
        if 'select_revision' in request.POST:
            # user has changed revistion number
            revision_form = RevisionForm(question, latest_revision, request.POST)
            if revision_form.is_valid():
                # Replace with those from the selected revision
                form = EditQuestionForm(question,
                                        QuestionRevision.objects.get(question=question,
                                        revision=revision_form.cleaned_data['revision']))
            else:
                form = EditQuestionForm(question, latest_revision, request.POST)
        else:
            # Always check modifications against the latest revision
            form = EditQuestionForm(question, latest_revision, request.POST)
            if form.is_valid():
                html = sanitize_html(markdowner.convert(form.cleaned_data['text']))
                if form.has_changed():
                    edited_at = datetime.datetime.now()
                    tags_changed = (latest_revision.tagnames !=
                                    form.cleaned_data['tags'])
                    tags_updated = False
                    # Update the Question itself
                    updated_fields = {
                        'title': form.cleaned_data['title'],
                        'last_edited_at': edited_at,
                        'last_edited_by': request.user,
                        'last_activity_at': edited_at,
                        'last_activity_by': request.user,
                        'tagnames': form.cleaned_data['tags'],
                        'summary': strip_tags(html)[:120],
                        'html': html,
                    }

                    # only save when it's checked
                    # because wiki doesn't allow to be edited if last version has been enabled already
                    # and we make sure this in forms.
                    if ('wiki' in form.cleaned_data and
                        form.cleaned_data['wiki']):
                        updated_fields['wiki'] = True
                        updated_fields['wikified_at'] = edited_at

                    Question.objects.filter(
                                            id=question.id).update(** updated_fields)
                    # Update the Question's tag associations
                    if tags_changed:
                        tags_updated = Question.objects.update_tags(
                                                                    question, form.cleaned_data['tags'], request.user)
                    # Create a new revision
                    revision = QuestionRevision(
                                                question=question,
                                                title=form.cleaned_data['title'],
                                                author=request.user,
                                                revised_at=edited_at,
                                                tagnames=form.cleaned_data['tags'],
                                                text=form.cleaned_data['text'],
                                                )
                    if form.cleaned_data['summary']:
                        revision.summary = form.cleaned_data['summary']
                    else:
                        revision.summary = 'No.%s Revision' % latest_revision.revision
                    revision.save()

                return HttpResponseRedirect(question.get_absolute_url())
    else:

        revision_form = RevisionForm(question, latest_revision)
        form = EditQuestionForm(question, latest_revision)
    return render_to_response('question_edit.html', {
                              'question': question,
                              'revision_form': revision_form,
                              'form': form,
                              'tags': _get_tags_cache_json()
                              }, context_instance=RequestContext(request))


@login_required
def edit_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    if answer.deleted and not can_view_deleted_post(request.user, answer):
        raise Http404
    elif not can_edit_post(request.user, answer):
        raise Http404
    else:
        latest_revision = answer.get_latest_revision()
        if request.method == "POST":
            if 'select_revision' in request.POST:
                # user has changed revistion number
                revision_form = RevisionForm(answer, latest_revision, request.POST)
                if revision_form.is_valid():
                    # Replace with those from the selected revision
                    form = EditAnswerForm(answer,
                                          AnswerRevision.objects.get(answer=answer,
                                          revision=revision_form.cleaned_data['revision']))
                else:
                    form = EditAnswerForm(answer, latest_revision, request.POST)
            else:
                form = EditAnswerForm(answer, latest_revision, request.POST)
                if form.is_valid():
                    html = sanitize_html(markdowner.convert(form.cleaned_data['text']))
                    if form.has_changed():
                        edited_at = datetime.datetime.now()
                        updated_fields = {
                            'last_edited_at': edited_at,
                            'last_edited_by': request.user,
                            'html': html,
                        }
                        Answer.objects.filter(id=answer.id).update(** updated_fields)

                        revision = AnswerRevision(
                                                  answer=answer,
                                                  author=request.user,
                                                  revised_at=edited_at,
                                                  text=form.cleaned_data['text']
                                                  )

                        if form.cleaned_data['summary']:
                            revision.summary = form.cleaned_data['summary']
                        else:
                            revision.summary = 'No.%s Revision' % latest_revision.revision
                        revision.save()

                        answer.question.last_activity_at = edited_at
                        answer.question.last_activity_by = request.user
                        answer.question.save()

                    return HttpResponseRedirect(answer.get_absolute_url())
        else:
            revision_form = RevisionForm(answer, latest_revision)
            form = EditAnswerForm(answer, latest_revision)
        return render_to_response('answer_edit.html', {
                                  'answer': answer,
                                  'revision_form': revision_form,
                                  'form': form,
                                  }, context_instance=RequestContext(request))

QUESTION_REVISION_TEMPLATE = ('<h1>%(title)s</h1>\n'
                              '<div class="text">%(html)s</div>\n'
                              '<div class="tags">%(tags)s</div>')
def question_revisions(request, id):
    post = get_object_or_404(Question, id=id)
    revisions = list(post.revisions.all())
    for i, revision in enumerate(revisions):
        revision.html = QUESTION_REVISION_TEMPLATE % {
            'title': revision.title,
            'html': sanitize_html(markdowner.convert(revision.text)),
            'tags': ' '.join(['<a class="post-tag">%s</a>' % tag
                             for tag in revision.tagnames.split(' ')]),
        }
        if i > 0:
            revisions[i - 1].diff = htmldiff(revision.html,
                                             revisions[i - 1].html)
        else:
            revisions[i - 1].diff = QUESTION_REVISION_TEMPLATE % {
                'title': revisions[0].title,
                'html': sanitize_html(markdowner.convert(revisions[0].text)),
                'tags': ' '.join(['<a class="post-tag">%s</a>' % tag
                                 for tag in revisions[0].tagnames.split(' ')]),
            }
            revisions[i - 1].summary = None
    return render_to_response('revisions_question.html', {
                              'post': post,
                              'revisions': revisions,
                              }, context_instance=RequestContext(request))

ANSWER_REVISION_TEMPLATE = ('<div class="text">%(html)s</div>')
def answer_revisions(request, id):
    post = get_object_or_404(Answer, id=id)
    revisions = list(post.revisions.all())
    for i, revision in enumerate(revisions):
        revision.html = ANSWER_REVISION_TEMPLATE % {
            'html': sanitize_html(markdowner.convert(revision.text))
        }
        if i > 0:
            revisions[i - 1].diff = htmldiff(revision.html,
                                             revisions[i - 1].html)
        else:
            revisions[i - 1].diff = revisions[i-1].text
            revisions[i - 1].summary = None
    return render_to_response('revisions_answer.html', {
                              'post': post,
                              'revisions': revisions,
                              }, context_instance=RequestContext(request))

def answer(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        form = AnswerForm(question, request.user, request.POST)
        if form.is_valid():
            wiki = form.cleaned_data['wiki']
            text = form.cleaned_data['text']
            update_time = datetime.datetime.now()

            if request.user.is_authenticated():
                create_new_answer(
                                  question=question,
                                  author=request.user,
                                  added_at=update_time,
                                  wiki=wiki,
                                  text=text,
                                  email_notify=form.cleaned_data['email_notify']
                                  )
            else:
                request.session.flush()
                html = sanitize_html(markdowner.convert(text))
                summary = strip_tags(html)[:120]
                anon = AnonymousAnswer(
                                       question=question,
                                       wiki=wiki,
                                       text=text,
                                       summary=summary,
                                       session_key=request.session.session_key,
                                       ip_addr=request.META['REMOTE_ADDR'],
                                       )
                anon.save()
                return HttpResponseRedirect('/account/signin/newanswer')

    return HttpResponseRedirect(question.get_absolute_url())

def tags(request):
    stag = ""
    is_paginated = True
    sortby = request.GET.get('sort', 'used')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    if request.method == "GET":
        stag = request.GET.get("q", "").strip()
        if len(stag) > 0:
            objects_list = Paginator(Tag.objects.filter(deleted=False).exclude(used_count=0).extra(where=['name like %s'], params=['%' + stag + '%']), DEFAULT_PAGE_SIZE)
        else:
            if sortby == "used":
                sortby = "-used_count"
            else:
                sortby = "name"
            objects_list = Paginator(Tag.objects.all().filter(deleted=False).exclude(used_count=0).order_by(sortby), DEFAULT_PAGE_SIZE)
    try:
        tags = objects_list.page(page)
    except (EmptyPage, InvalidPage):
        tags = objects_list.page(objects_list.num_pages)

    return render_to_response('tags.html', {
                              "tags": tags,
                              "stag": stag,
                              "tab_id": sortby,
                              "keywords": stag,
                              "context": {
                              'is_paginated': is_paginated,
                              'pages': objects_list.num_pages,
                              'page': page,
                              'has_previous': tags.has_previous(),
                              'has_next': tags.has_next(),
                              'previous': tags.previous_page_number(),
                              'next': tags.next_page_number(),
                              'base_url': '/tags/?sort=%s&' % sortby
                              }

                              }, context_instance=RequestContext(request))

def tag(request, tag):
    return questions(request, tagname=tag)

def vote(request, id):
    """
    vote_type:
        acceptAnswer : 0,
        questionUpVote : 1,
        questionDownVote : 2,
        favorite : 4,
        answerUpVote: 5,
        answerDownVote:6,
        offensiveQuestion : 7,
        offensiveAnswer:8,
        removeQuestion: 9,
        removeAnswer:10
        questionSubscribeUpdates:11

    accept answer code:
        response_data['allowed'] = -1, Accept his own answer   0, no allowed - Anonymous    1, Allowed - by default
        response_data['success'] =  0, failed                                               1, Success - by default
        response_data['status']  =  0, By default                                           1, Answer has been accepted already(Cancel)

    vote code:
        allowed = -3, Don't have enough votes left
                  -2, Don't have enough reputation score
                  -1, Vote his own post
                   0, no allowed - Anonymous
                   1, Allowed - by default
        status  =  0, By default
                   1, Cancel
                   2, Vote is too old to be canceled

    offensive code:
        allowed = -3, Don't have enough flags left
                  -2, Don't have enough reputation score to do this
                   0, not allowed
                   1, allowed
        status  =  0, by default
                   1, can't do it again
    """
    response_data = {
        "allowed": 1,
        "success": 1,
        "status": 0,
        "count": 0,
        "message": ''
    }

    def can_vote(vote_score, user):
        if vote_score == 1:
            return can_vote_up(request.user)
        else:
            return can_vote_down(request.user)

    try:
        if not request.user.is_authenticated():
            response_data['allowed'] = 0
            response_data['success'] = 0

        elif request.is_ajax():
            question = get_object_or_404(Question, id=id)
            vote_type = request.POST.get('type')

            #accept answer
            if vote_type == '0':
                answer_id = request.POST.get('postId')
                answer = get_object_or_404(Answer, id=answer_id)
                # make sure question author is current user
                if question.author == request.user:
                    # answer user who is also question author is not allow to accept answer
                    if answer.author == question.author:
                        response_data['success'] = 0
                        response_data['allowed'] = -1
                    # check if answer has been accepted already
                    elif answer.accepted:
                        onAnswerAcceptCanceled(answer, request.user)
                        response_data['status'] = 1
                    else:
                        # set other answers in this question not accepted first
                        for answer_of_question in Answer.objects.get_answers_from_question(question, request.user):
                            if answer_of_question != answer and answer_of_question.accepted:
                                onAnswerAcceptCanceled(answer_of_question, request.user)

                        #make sure retrieve data again after above author changes, they may have related data
                        answer = get_object_or_404(Answer, id=answer_id)
                        onAnswerAccept(answer, request.user)
                else:
                    response_data['allowed'] = 0
                    response_data['success'] = 0
            # favorite
            elif vote_type == '4':
                has_favorited = False
                fav_questions = FavoriteQuestion.objects.filter(question=question)
                # if the same question has been favorited before, then delete it
                if fav_questions is not None:
                    for item in fav_questions:
                        if item.user == request.user:
                            item.delete()
                            response_data['status'] = 1
                            response_data['count']  = len(fav_questions) - 1
                            if response_data['count'] < 0:
                                response_data['count'] = 0
                            has_favorited = True
                # if above deletion has not been executed, just insert a new favorite question
                if not has_favorited:
                    new_item = FavoriteQuestion(question=question, user=request.user)
                    new_item.save()
                    response_data['count']  = FavoriteQuestion.objects.filter(question=question).count()
                Question.objects.update_favorite_count(question)

            elif vote_type in ['1', '2', '5', '6']:
                post_id = id
                post = question
                vote_score = 1
                if vote_type in ['5', '6']:
                    answer_id = request.POST.get('postId')
                    answer = get_object_or_404(Answer, id=answer_id)
                    post_id = answer_id
                    post = answer
                if vote_type in ['2', '6']:
                    vote_score = -1

                if post.author == request.user:
                    response_data['allowed'] = -1
                elif not can_vote(vote_score, request.user):
                    response_data['allowed'] = -2
                elif post.votes.filter(user=request.user).count() > 0:
                    vote = post.votes.filter(user=request.user)[0]
                    # unvote should be less than certain time
                    if (datetime.datetime.now().day - vote.voted_at.day) >= VOTE_RULES['scope_deny_unvote_days']:
                        response_data['status'] = 2
                    else:
                        voted = vote.vote
                        if voted > 0:
                            # cancel upvote
                            onUpVotedCanceled(vote, post, request.user)

                        else:
                            # cancel downvote
                            onDownVotedCanceled(vote, post, request.user)

                        response_data['status'] = 1
                        response_data['count'] = post.score
                elif Vote.objects.get_votes_count_today_from_user(request.user) >= VOTE_RULES['scope_votes_per_user_per_day']:
                    response_data['allowed'] = -3
                else:
                    vote = Vote(user=request.user, content_object=post, vote=vote_score, voted_at=datetime.datetime.now())
                    if vote_score > 0:
                        # upvote
                        onUpVoted(vote, post, request.user)
                    else:
                        # downvote
                        onDownVoted(vote, post, request.user)

                    votes_left = VOTE_RULES['scope_votes_per_user_per_day'] - Vote.objects.get_votes_count_today_from_user(request.user)
                    if votes_left <= VOTE_RULES['scope_warn_votes_left']:
                        response_data['message'] = u'%s votes left' % votes_left
                    response_data['count'] = post.score
            elif vote_type in ['7', '8']:
                post = question
                post_id = id
                if vote_type == '8':
                    post_id = request.POST.get('postId')
                    post = get_object_or_404(Answer, id=post_id)

                if FlaggedItem.objects.get_flagged_items_count_today(request.user) >= VOTE_RULES['scope_flags_per_user_per_day']:
                    response_data['allowed'] = -3
                elif not can_flag_offensive(request.user):
                    response_data['allowed'] = -2
                elif post.flagged_items.filter(user=request.user).count() > 0:
                    response_data['status'] = 1
                else:
                    item = FlaggedItem(user=request.user, content_object=post, flagged_at=datetime.datetime.now())
                    onFlaggedItem(item, post, request.user)
                    response_data['count'] = post.offensive_flag_count
                    # send signal when question or answer be marked offensive
                    mark_offensive.send(sender=post.__class__, instance=post, mark_by=request.user)
            elif vote_type in ['9', '10']:
                post = question
                post_id = id
                if vote_type == '10':
                    post_id = request.POST.get('postId')
                    post = get_object_or_404(Answer, id=post_id)

                if not can_delete_post(request.user, post):
                    response_data['allowed'] = -2
                elif post.deleted:
                    onDeleteCanceled(post, request.user)
                    response_data['status'] = 1
                else:
                    onDeleted(post, request.user)
                    delete_post_or_answer.send(sender=post.__class__, instance=post, delete_by=request.user)
            elif vote_type == '11':#subscribe q updates
                user = request.user
                if user.is_authenticated():
                    try:
                        EmailFeed.objects.get(feed_id=question.id, subscriber_id=user.id, feed_content_type=question_type)
                    except EmailFeed.DoesNotExist:
                        feed = EmailFeed(subscriber=user, content=question)
                        feed.save()
                        if settings.EMAIL_VALIDATION == 'on' and user.email_isvalid == False:
                            response_data['message'] = _('subscription saved, %(email)s needs validation') % {'email':user.email}
                    #response_data['status'] = 1
                    #responst_data['allowed'] = 1
                else:
                    pass
                    #response_data['status'] = 0
                    #response_data['allowed'] = 0
            elif vote_type == '12':#unsubscribe q updates
                user = request.user
                if user.is_authenticated():
                    try:
                        feed = EmailFeed.objects.get(feed_id=question.id, subscriber_id=user.id)
                        feed.delete()
                    except EmailFeed.DoesNotExist:
                        pass
                    
        else:
            response_data['success'] = 0
            response_data['message'] = u'Request mode is not supported. Please try again.'

        data = simplejson.dumps(response_data)

    except Exception, e:
        response_data['message'] = str(e)
        data = simplejson.dumps(response_data)
    return HttpResponse(data, mimetype="application/json")

def users(request):
    is_paginated = True
    sortby = request.GET.get('sort', 'reputation')
    suser = request.REQUEST.get('q', "")
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    if suser == "":
        if sortby == "newest":
            objects_list = Paginator(User.objects.all().order_by('-date_joined'), USERS_PAGE_SIZE)
        elif sortby == "last":
            objects_list = Paginator(User.objects.all().order_by('date_joined'), USERS_PAGE_SIZE)
        elif sortby == "user":
            objects_list = Paginator(User.objects.all().order_by('username'), USERS_PAGE_SIZE)
        # default
        else:
            objects_list = Paginator(User.objects.all().order_by('-reputation'), USERS_PAGE_SIZE)
        base_url = '/users/?sort=%s&' % sortby
    else:
        sortby = "reputation"
        objects_list = Paginator(User.objects.extra(where=['username like %s'], params=['%' + suser + '%']).order_by('-reputation'), USERS_PAGE_SIZE)
        base_url = '/users/?name=%s&sort=%s&' % (suser, sortby)

    try:
        users = objects_list.page(page)
    except (EmptyPage, InvalidPage):
        users = objects_list.page(objects_list.num_pages)

    return render_to_response('users.html', {
                              "users": users,
                              "suser": suser,
                              "keywords": suser,
                              "tab_id": sortby,
                              "context": {
                              'is_paginated': is_paginated,
                              'pages': objects_list.num_pages,
                              'page': page,
                              'has_previous': users.has_previous(),
                              'has_next': users.has_next(),
                              'previous': users.previous_page_number(),
                              'next': users.next_page_number(),
                              'base_url': base_url
                              }

                              }, context_instance=RequestContext(request))

def user(request, id):
    sort = request.GET.get('sort', 'stats')
    user_view = dict((v.id, v) for v in USER_TEMPLATE_VIEWS).get(sort, USER_TEMPLATE_VIEWS[0])
    from forum import views
    func = getattr(views, user_view.view_name)
    return func(request, id, user_view)

@login_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.user != user:
        raise Http404
    if request.method == "POST":
        form = EditUserForm(user, request.POST)
        if form.is_valid():
            new_email = sanitize_html(form.cleaned_data['email'])

            from django_authopenid.views import set_new_email
            set_new_email(user, new_email)

            user.real_name = sanitize_html(form.cleaned_data['realname'])
            user.website = sanitize_html(form.cleaned_data['website'])
            user.location = sanitize_html(form.cleaned_data['city'])
            user.date_of_birth = sanitize_html(form.cleaned_data['birthday'])
            if len(user.date_of_birth) == 0:
                user.date_of_birth = '1900-01-01'
            user.about = sanitize_html(form.cleaned_data['about'])

            user.save()
            # send user updated singal if full fields have been updated
            if user.email and user.real_name and user.website and user.location and \
                user.date_of_birth and user.about:
                user_updated.send(sender=user.__class__, instance=user, updated_by=user)
            return HttpResponseRedirect(user.get_profile_url())
    else:
        form = EditUserForm(user)
    return render_to_response('user_edit.html', {
                              'form': form,
                              }, context_instance=RequestContext(request))

def user_stats(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    questions = Question.objects.extra(
                                       select={
                                       'vote_count': 'question.score',
                                       'favorited_myself': 'SELECT count(*) FROM favorite_question f WHERE f.user_id = %s AND f.question_id = question.id',
                                       'la_user_id': 'auth_user.id',
                                       'la_username': 'auth_user.username',
                                       'la_user_gold': 'auth_user.gold',
                                       'la_user_silver': 'auth_user.silver',
                                       'la_user_bronze': 'auth_user.bronze',
                                       'la_user_reputation': 'auth_user.reputation'
                                       },
                                       select_params=[user_id],
                                       tables=['question', 'auth_user'],
                                       where=['question.deleted = 0 AND question.author_id=%s AND question.last_activity_by_id = auth_user.id'],
                                       params=[user_id],
                                       order_by=['-vote_count', '-last_activity_at']
                                       ).values('vote_count',
        'favorited_myself',
        'id',
        'title',
        'author_id',
        'added_at',
        'answer_accepted',
        'answer_count',
        'comment_count',
        'view_count',
        'favourite_count',
        'summary',
        'tagnames',
        'vote_up_count',
        'vote_down_count',
        'last_activity_at',
        'la_user_id',
        'la_username',
        'la_user_gold',
        'la_user_silver',
        'la_user_bronze',
        'la_user_reputation')[:100]

    answered_questions = Question.objects.extra(
                                                select={
                                                'vote_up_count': 'answer.vote_up_count',
                                                'vote_down_count': 'answer.vote_down_count',
                                                'answer_id': 'answer.id',
                                                'accepted': 'answer.accepted',
                                                'vote_count': 'answer.score',
                                                'comment_count': 'answer.comment_count'
                                                },
                                                tables=['question', 'answer'],
                                                where=['answer.deleted=0 AND answer.author_id=%s AND answer.question_id=question.id'],
                                                params=[user_id],
                                                order_by=['-vote_count', '-answer_id'],
                                                select_params=[user_id]
                                                ).distinct().values('comment_count',
                   'id',
                   'answer_id',
                   'title',
                   'author_id',
                   'accepted',
                   'vote_count',
                   'answer_count',
                   'vote_up_count',
                   'vote_down_count')[:100]
    up_votes = Vote.objects.get_up_vote_count_from_user(user)
    down_votes = Vote.objects.get_down_vote_count_from_user(user)
    votes_today = Vote.objects.get_votes_count_today_from_user(user)
    votes_total = VOTE_RULES['scope_votes_per_user_per_day']
    tags = user.created_tags.all().order_by('-used_count')[:50]
    try:
        from django.db.models import Count
        awards = Award.objects.extra(
                                     select={'id': 'badge.id', 'name':'badge.name', 'description': 'badge.description', 'type': 'badge.type'},
                                     tables=['award', 'badge'],
                                     order_by=['-awarded_at'],
                                     where=['user_id=%s AND badge_id=badge.id'],
                                     params=[user.id]
                                     ).values('id', 'name', 'description', 'type')
        total_awards = awards.count()
        awards = awards.annotate(count=Count('badge__id'))
    except ImportError:
        awards = Award.objects.extra(
                                     select={'id': 'badge.id', 'count': 'count(badge_id)', 'name':'badge.name', 'description': 'badge.description', 'type': 'badge.type'},
                                     tables=['award', 'badge'],
                                     order_by=['-awarded_at'],
                                     where=['user_id=%s AND badge_id=badge.id'],
                                     params=[user.id]
                                     ).values('id', 'count', 'name', 'description', 'type')
        total_awards = awards.count()
        awards.query.group_by = ['badge_id']


    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              "questions": questions,
                              "answered_questions": answered_questions,
                              "up_votes": up_votes,
                              "down_votes": down_votes,
                              "total_votes": up_votes + down_votes,
                              "votes_today_left": votes_total-votes_today,
                              "votes_total_per_day": votes_total,
                              "tags": tags,
                              "awards": awards,
                              "total_awards": total_awards,
                              }, context_instance=RequestContext(request))

def user_recent(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    def get_type_name(type_id):
        for item in TYPE_ACTIVITY:
            if type_id in item:
                return item[1]

    class Event:
        def __init__(self, time, type, title, summary, answer_id, question_id):
            self.time = time
            self.type = get_type_name(type)
            self.type_id = type
            self.title = title
            self.summary = summary
            self.title_link = u'/questions/%s/%s#%s' % (question_id, title, answer_id)\
                if int(answer_id) > 0 else u'/questions/%s/%s' % (question_id, title)
    class AwardEvent:
        def __init__(self, time, type, id):
            self.time = time
            self.type = get_type_name(type)
            self.type_id = type
            self.badge = get_object_or_404(Badge, id=id)

    activities = []
    # ask questions
    questions = Activity.objects.extra(
                                       select={
                                       'title': 'question.title',
                                       'question_id': 'question.id',
                                       'active_at': 'activity.active_at',
                                       'activity_type': 'activity.activity_type'
                                       },
                                       tables=['activity', 'question'],
                                       where=['activity.content_type_id = %s AND activity.object_id = ' +
                                       'question.id AND activity.user_id = %s AND activity.activity_type = %s'],
                                       params=[question_type_id, user_id, TYPE_ACTIVITY_ASK_QUESTION],
                                       order_by=['-activity.active_at']
                                       ).values(
        'title',
        'question_id',
        'active_at',
        'activity_type'
        )
    if len(questions) > 0:
        questions = [(Event(q['active_at'], q['activity_type'], q['title'], '', '0', \
                      q['question_id'])) for q in questions]
        activities.extend(questions)

    # answers
    answers = Activity.objects.extra(
                                     select={
                                     'title': 'question.title',
                                     'question_id': 'question.id',
                                     'answer_id': 'answer.id',
                                     'active_at': 'activity.active_at',
                                     'activity_type': 'activity.activity_type'
                                     },
                                     tables=['activity', 'answer', 'question'],
                                     where=['activity.content_type_id = %s AND activity.object_id = answer.id AND ' +
                                     'answer.question_id=question.id AND activity.user_id=%s AND activity.activity_type=%s'],
                                     params=[answer_type_id, user_id, TYPE_ACTIVITY_ANSWER],
                                     order_by=['-activity.active_at']
                                     ).values(
        'title',
        'question_id',
        'answer_id',
        'active_at',
        'activity_type'
        )
    if len(answers) > 0:
        answers = [(Event(q['active_at'], q['activity_type'], q['title'], '', q['answer_id'], \
                    q['question_id'])) for q in answers]
        activities.extend(answers)

    # question comments
    comments = Activity.objects.extra(
                                      select={
                                      'title': 'question.title',
                                      'question_id': 'comment.object_id',
                                      'added_at': 'comment.added_at',
                                      'activity_type': 'activity.activity_type'
                                      },
                                      tables=['activity', 'question', 'comment'],

                                      where=['activity.content_type_id = %s AND activity.object_id = comment.id AND ' +
                                      'activity.user_id = comment.user_id AND comment.object_id=question.id AND ' +
                                      'comment.content_type_id=%s AND activity.user_id = %s AND activity.activity_type=%s'],
                                      params=[comment_type_id, question_type_id, user_id, TYPE_ACTIVITY_COMMENT_QUESTION],
                                      order_by=['-comment.added_at']
                                      ).values(
        'title',
        'question_id',
        'added_at',
        'activity_type'
        )

    if len(comments) > 0:
        comments = [(Event(q['added_at'], q['activity_type'], q['title'], '', '0', \
                     q['question_id'])) for q in comments]
        activities.extend(comments)

    # answer comments
    comments = Activity.objects.extra(
                                      select={
                                      'title': 'question.title',
                                      'question_id': 'question.id',
                                      'answer_id': 'answer.id',
                                      'added_at': 'comment.added_at',
                                      'activity_type': 'activity.activity_type'
                                      },
                                      tables=['activity', 'question', 'answer', 'comment'],

                                      where=['activity.content_type_id = %s AND activity.object_id = comment.id AND ' +
                                      'activity.user_id = comment.user_id AND comment.object_id=answer.id AND ' +
                                      'comment.content_type_id=%s AND question.id = answer.question_id AND ' +
                                      'activity.user_id = %s AND activity.activity_type=%s'],
                                      params=[comment_type_id, answer_type_id, user_id, TYPE_ACTIVITY_COMMENT_ANSWER],
                                      order_by=['-comment.added_at']
                                      ).values(
        'title',
        'question_id',
        'answer_id',
        'added_at',
        'activity_type'
        )

    if len(comments) > 0:
        comments = [(Event(q['added_at'], q['activity_type'], q['title'], '', q['answer_id'], \
                     q['question_id'])) for q in comments]
        activities.extend(comments)

    # question revisions
    revisions = Activity.objects.extra(
                                       select={
                                       'title': 'question_revision.title',
                                       'question_id': 'question_revision.question_id',
                                       'added_at': 'activity.active_at',
                                       'activity_type': 'activity.activity_type',
                                       'summary': 'question_revision.summary'
                                       },
                                       tables=['activity', 'question_revision'],
                                       where=['activity.content_type_id = %s AND activity.object_id = question_revision.id AND ' +
                                       'activity.user_id = question_revision.author_id AND activity.user_id = %s AND ' +
                                       'activity.activity_type=%s'],
                                       params=[question_revision_type_id, user_id, TYPE_ACTIVITY_UPDATE_QUESTION],
                                       order_by=['-activity.active_at']
                                       ).values(
        'title',
        'question_id',
        'added_at',
        'activity_type',
        'summary'
        )

    if len(revisions) > 0:
        revisions = [(Event(q['added_at'], q['activity_type'], q['title'], q['summary'], '0', \
                      q['question_id'])) for q in revisions]
        activities.extend(revisions)

    # answer revisions
    revisions = Activity.objects.extra(
                                       select={
                                       'title': 'question.title',
                                       'question_id': 'question.id',
                                       'answer_id': 'answer.id',
                                       'added_at': 'activity.active_at',
                                       'activity_type': 'activity.activity_type',
                                       'summary': 'answer_revision.summary'
                                       },
                                       tables=['activity', 'answer_revision', 'question', 'answer'],

                                       where=['activity.content_type_id = %s AND activity.object_id = answer_revision.id AND ' +
                                       'activity.user_id = answer_revision.author_id AND activity.user_id = %s AND ' +
                                       'answer_revision.answer_id=answer.id AND answer.question_id = question.id AND ' +
                                       'activity.activity_type=%s'],
                                       params=[answer_revision_type_id, user_id, TYPE_ACTIVITY_UPDATE_ANSWER],
                                       order_by=['-activity.active_at']
                                       ).values(
        'title',
        'question_id',
        'added_at',
        'answer_id',
        'activity_type',
        'summary'
        )

    if len(revisions) > 0:
        revisions = [(Event(q['added_at'], q['activity_type'], q['title'], q['summary'], \
                      q['answer_id'], q['question_id'])) for q in revisions]
        activities.extend(revisions)

    # accepted answers
    accept_answers = Activity.objects.extra(
                                            select={
                                            'title': 'question.title',
                                            'question_id': 'question.id',
                                            'added_at': 'activity.active_at',
                                            'activity_type': 'activity.activity_type',
                                            },
                                            tables=['activity', 'answer', 'question'],
                                            where=['activity.content_type_id = %s AND activity.object_id = answer.id AND ' +
                                            'activity.user_id = question.author_id AND activity.user_id = %s AND ' +
                                            'answer.question_id=question.id AND activity.activity_type=%s'],
                                            params=[answer_type_id, user_id, TYPE_ACTIVITY_MARK_ANSWER],
                                            order_by=['-activity.active_at']
                                            ).values(
        'title',
        'question_id',
        'added_at',
        'activity_type',
        )
    if len(accept_answers) > 0:
        accept_answers = [(Event(q['added_at'], q['activity_type'], q['title'], '', '0', \
                           q['question_id'])) for q in accept_answers]
        activities.extend(accept_answers)
    #award history
    awards = Activity.objects.extra(
                                    select={
                                    'badge_id': 'badge.id',
                                    'awarded_at': 'award.awarded_at',
                                    'activity_type': 'activity.activity_type'
                                    },
                                    tables=['activity', 'award', 'badge'],
                                    where=['activity.user_id = award.user_id AND activity.user_id = %s AND ' +
                                    'award.badge_id=badge.id AND activity.object_id=award.id AND activity.activity_type=%s'],
                                    params=[user_id, TYPE_ACTIVITY_PRIZE],
                                    order_by=['-activity.active_at']
                                    ).values(
        'badge_id',
        'awarded_at',
        'activity_type'
        )
    if len(awards) > 0:
        awards = [(AwardEvent(q['awarded_at'], q['activity_type'], q['badge_id'])) for q in awards]
        activities.extend(awards)

    activities.sort(lambda x, y: cmp(y.time, x.time))

    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              "activities": activities[:user_view.data_size]
                              }, context_instance=RequestContext(request))

def user_responses(request, user_id, user_view):
    """
    We list answers for question, comments, and answer accepted by others for this user.
    """
    class Response:
        def __init__(self, type, title, question_id, answer_id, time, username, user_id, content):
            self.type = type
            self.title = title
            self.titlelink = u'/questions/%s/%s#%s' % (question_id, title, answer_id)
            self.time = time
            self.userlink = u'/users/%s/%s/' % (user_id, username)
            self.username = username
            self.content = u'%s ...' % strip_tags(content)[:300]

        def __unicode__(self):
            return u'%s %s' % (self.type, self.titlelink)

    user = get_object_or_404(User, id=user_id)
    responses = []
    answers = Answer.objects.extra(
                                   select={
                                   'title': 'question.title',
                                   'question_id': 'question.id',
                                   'answer_id': 'answer.id',
                                   'added_at': 'answer.added_at',
                                   'html': 'answer.html',
                                   'username': 'auth_user.username',
                                   'user_id': 'auth_user.id'
                                   },
                                   select_params=[user_id],
                                   tables=['answer', 'question', 'auth_user'],
                                   where=['answer.question_id = question.id AND answer.deleted=0 AND question.deleted = 0 AND ' +
                                   'question.author_id = %s AND answer.author_id <> %s AND answer.author_id=auth_user.id'],
                                   params=[user_id, user_id],
                                   order_by=['-answer.id']
                                   ).values(
        'title',
        'question_id',
        'answer_id',
        'added_at',
        'html',
        'username',
        'user_id'
        )
    if len(answers) > 0:
        answers = [(Response(TYPE_RESPONSE['QUESTION_ANSWERED'], a['title'], a['question_id'],
                    a['answer_id'], a['added_at'], a['username'], a['user_id'], a['html'])) for a in answers]
        responses.extend(answers)


    # question comments
    comments = Comment.objects.extra(
                                     select={
                                     'title': 'question.title',
                                     'question_id': 'comment.object_id',
                                     'added_at': 'comment.added_at',
                                     'comment': 'comment.comment',
                                     'username': 'auth_user.username',
                                     'user_id': 'auth_user.id'
                                     },
                                     tables=['question', 'auth_user', 'comment'],
                                     where=['question.deleted = 0 AND question.author_id = %s AND comment.object_id=question.id AND ' +
                                     'comment.content_type_id=%s AND comment.user_id <> %s AND comment.user_id = auth_user.id'],
                                     params=[user_id, question_type_id, user_id],
                                     order_by=['-comment.added_at']
                                     ).values(
        'title',
        'question_id',
        'added_at',
        'comment',
        'username',
        'user_id'
        )

    if len(comments) > 0:
        comments = [(Response(TYPE_RESPONSE['QUESTION_COMMENTED'], c['title'], c['question_id'],
                     '', c['added_at'], c['username'], c['user_id'], c['comment'])) for c in comments]
        responses.extend(comments)

    # answer comments
    comments = Comment.objects.extra(
                                     select={
                                     'title': 'question.title',
                                     'question_id': 'question.id',
                                     'answer_id': 'answer.id',
                                     'added_at': 'comment.added_at',
                                     'comment': 'comment.comment',
                                     'username': 'auth_user.username',
                                     'user_id': 'auth_user.id'
                                     },
                                     tables=['answer', 'auth_user', 'comment', 'question'],
                                     where=['answer.deleted = 0 AND answer.author_id = %s AND comment.object_id=answer.id AND ' +
                                     'comment.content_type_id=%s AND comment.user_id <> %s AND comment.user_id = auth_user.id ' +
                                     'AND question.id = answer.question_id'],
                                     params=[user_id, answer_type_id, user_id],
                                     order_by=['-comment.added_at']
                                     ).values(
        'title',
        'question_id',
        'answer_id',
        'added_at',
        'comment',
        'username',
        'user_id'
        )

    if len(comments) > 0:
        comments = [(Response(TYPE_RESPONSE['ANSWER_COMMENTED'], c['title'], c['question_id'],
                     c['answer_id'], c['added_at'], c['username'], c['user_id'], c['comment'])) for c in comments]
        responses.extend(comments)

    # answer has been accepted
    answers = Answer.objects.extra(
                                   select={
                                   'title': 'question.title',
                                   'question_id': 'question.id',
                                   'answer_id': 'answer.id',
                                   'added_at': 'answer.accepted_at',
                                   'html': 'answer.html',
                                   'username': 'auth_user.username',
                                   'user_id': 'auth_user.id'
                                   },
                                   select_params=[user_id],
                                   tables=['answer', 'question', 'auth_user'],
                                   where=['answer.question_id = question.id AND answer.deleted=0 AND question.deleted = 0 AND ' +
                                   'answer.author_id = %s AND answer.accepted=1 AND question.author_id=auth_user.id'],
                                   params=[user_id],
                                   order_by=['-answer.id']
                                   ).values(
        'title',
        'question_id',
        'answer_id',
        'added_at',
        'html',
        'username',
        'user_id'
        )
    if len(answers) > 0:
        answers = [(Response(TYPE_RESPONSE['ANSWER_ACCEPTED'], a['title'], a['question_id'],
                    a['answer_id'], a['added_at'], a['username'], a['user_id'], a['html'])) for a in answers]
        responses.extend(answers)

    # sort posts by time
    responses.sort(lambda x, y: cmp(y.time, x.time))

    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              "responses": responses[:user_view.data_size],

                              }, context_instance=RequestContext(request))

def user_votes(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    if not can_view_user_votes(request.user, user):
        raise Http404
    votes = []
    question_votes = Vote.objects.extra(
                                        select={
                                        'title': 'question.title',
                                        'question_id': 'question.id',
                                        'answer_id': 0,
                                        'voted_at': 'vote.voted_at',
                                        'vote': 'vote',
                                        },
                                        select_params=[user_id],
                                        tables=['vote', 'question', 'auth_user'],
                                        where=['vote.content_type_id = %s AND vote.user_id = %s AND vote.object_id = question.id ' +
                                        'AND vote.user_id=auth_user.id'],
                                        params=[question_type_id, user_id],
                                        order_by=['-vote.id']
                                        ).values(
        'title',
        'question_id',
        'answer_id',
        'voted_at',
        'vote',
        )
    if(len(question_votes) > 0):
        votes.extend(question_votes)

    answer_votes = Vote.objects.extra(
                                      select={
                                      'title': 'question.title',
                                      'question_id': 'question.id',
                                      'answer_id': 'answer.id',
                                      'voted_at': 'vote.voted_at',
                                      'vote': 'vote',
                                      },
                                      select_params=[user_id],
                                      tables=['vote', 'answer', 'question', 'auth_user'],
                                      where=['vote.content_type_id = %s AND vote.user_id = %s AND vote.object_id = answer.id ' +
                                      'AND answer.question_id = question.id AND vote.user_id=auth_user.id'],
                                      params=[answer_type_id, user_id],
                                      order_by=['-vote.id']
                                      ).values(
        'title',
        'question_id',
        'answer_id',
        'voted_at',
        'vote',
        )
    if(len(answer_votes) > 0):
        votes.extend(answer_votes)
    votes.sort(lambda x, y: cmp(y['voted_at'], x['voted_at']))
    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              "votes": votes[:user_view.data_size]

                              }, context_instance=RequestContext(request))

def user_reputation(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    try:
        from django.db.models import Sum
        reputation = Repute.objects.extra(
                                          select={'question_id':'question_id',
                                          'title': 'question.title'},
                                          tables=['repute', 'question'],
                                          order_by=['-reputed_at'],
                                          where=['user_id=%s AND question_id=question.id'],
                                          params=[user.id]
                                          ).values('question_id', 'title', 'reputed_at', 'reputation')
        reputation = reputation.annotate(positive=Sum("positive"), negative=Sum("negative"))
    except ImportError:
        reputation = Repute.objects.extra(
                                          select={'positive':'sum(positive)', 'negative':'sum(negative)', 'question_id':'question_id',
                                          'title': 'question.title'},
                                          tables=['repute', 'question'],
                                          order_by=['-reputed_at'],
                                          where=['user_id=%s AND question_id=question.id'],
                                          params=[user.id]
                                          ).values('positive', 'negative', 'question_id', 'title', 'reputed_at', 'reputation')
        reputation.query.group_by = ['question_id']

    rep_list = []
    for rep in Repute.objects.filter(user=user).order_by('reputed_at'):
        dic = '[%s,%s]' % (calendar.timegm(rep.reputed_at.timetuple()) * 1000, rep.reputation)
        rep_list.append(dic)
    reps = ','.join(rep_list)
    reps = '[%s]' % reps

    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              "reputation": reputation,
                              "reps": reps
                              }, context_instance=RequestContext(request))

def user_favorites(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    questions = Question.objects.extra(
                                       select={
                                       'vote_count': 'question.vote_up_count + question.vote_down_count',
                                       'favorited_myself': 'SELECT count(*) FROM favorite_question f WHERE f.user_id = %s ' +
                                       'AND f.question_id = question.id',
                                       'la_user_id': 'auth_user.id',
                                       'la_username': 'auth_user.username',
                                       'la_user_gold': 'auth_user.gold',
                                       'la_user_silver': 'auth_user.silver',
                                       'la_user_bronze': 'auth_user.bronze',
                                       'la_user_reputation': 'auth_user.reputation'
                                       },
                                       select_params=[user_id],
                                       tables=['question', 'auth_user', 'favorite_question'],
                                       where=['question.deleted = 0 AND question.last_activity_by_id = auth_user.id ' +
                                       'AND favorite_question.question_id = question.id AND favorite_question.user_id = %s'],
                                       params=[user_id],
                                       order_by=['-vote_count', '-question.id']
                                       ).values('vote_count',
        'favorited_myself',
        'id',
        'title',
        'author_id',
        'added_at',
        'answer_accepted',
        'answer_count',
        'comment_count',
        'view_count',
        'favourite_count',
        'summary',
        'tagnames',
        'vote_up_count',
        'vote_down_count',
        'last_activity_at',
        'la_user_id',
        'la_username',
        'la_user_gold',
        'la_user_silver',
        'la_user_bronze',
        'la_user_reputation')
    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "questions": questions[:user_view.data_size],
                              "view_user": user
                              }, context_instance=RequestContext(request))


def user_preferences(request, user_id, user_view):
    user = get_object_or_404(User, id=user_id)
    return render_to_response(user_view.template_file, {
                              "tab_name": user_view.id,
                              "tab_description": user_view.tab_description,
                              "page_title": user_view.page_title,
                              "view_user": user,
                              }, context_instance=RequestContext(request))

def question_comments(request, id):
    question = get_object_or_404(Question, id=id)
    user = request.user
    return __comments(request, question, 'question', user)

def answer_comments(request, id):
    answer = get_object_or_404(Answer, id=id)
    user = request.user
    return __comments(request, answer, 'answer', user)

def __comments(request, obj, type, user):
    # only support get comments by ajax now
    if request.is_ajax():
        if request.method == "GET":
            return __generate_comments_json(obj, type, user)
        elif request.method == "POST":
            comment_data = request.POST.get('comment')
            comment = Comment(content_object=obj, comment=comment_data, user=request.user)
            comment.save()
            obj.comment_count = obj.comment_count + 1
            obj.save()
            return __generate_comments_json(obj, type, user)

def __generate_comments_json(obj, type, user):
    comments = obj.comments.all().order_by('-id')
    # {"Id":6,"PostId":38589,"CreationDate":"an hour ago","Text":"hello there!","UserDisplayName":"Jarrod Dixon","UserUrl":"/users/3/jarrod-dixon","DeleteUrl":null}
    json_comments = []
    for comment in comments:
        comment_user = comment.user
        delete_url = ""
        if user != None and auth.can_delete_comment(user, comment):
            #/posts/392845/comments/219852/delete
            delete_url = "/" + type + "s/%s/comments/%s/delete/" % (obj.id, comment.id)
        json_comments.append({"id": comment.id,
                             "object_id": obj.id,
                             "add_date": comment.added_at.strftime('%Y-%m-%d'),
                             "text": comment.comment,
                             "user_display_name": comment_user.username,
                             "user_url": "/users/%s/%s" % (comment_user.id, comment_user.username),
                             "delete_url": delete_url
                             })

    data = simplejson.dumps(json_comments)
    return HttpResponse(data, mimetype="application/json")

def delete_question_comment(request, question_id, comment_id):
    if request.is_ajax():
        question = get_object_or_404(Question, id=question_id)
        comment = get_object_or_404(Comment, id=comment_id)

        question.comments.remove(comment)
        question.comment_count = question.comment_count - 1
        question.save()
        user = request.user
        return __generate_comments_json(question, 'question', user)

def delete_answer_comment(request, answer_id, comment_id):
    if request.is_ajax():
        answer = get_object_or_404(Answer, id=answer_id)
        comment = get_object_or_404(Comment, id=comment_id)

        answer.comments.remove(comment)
        answer.comment_count = answer.comment_count - 1
        answer.save()
        user = request.user
        return __generate_comments_json(answer, 'answer', user)

def logout(request):
    url = request.GET.get('next')
    return render_to_response('logout.html', {
                              'next': url,
                              }, context_instance=RequestContext(request))

def badges(request):
    badges = Badge.objects.all().order_by('type')
    my_badges = []
    if request.user.is_authenticated():
        my_badges = Award.objects.filter(user=request.user)
        my_badges.query.group_by = ['badge_id']

    return render_to_response('badges.html', {
                              'badges': badges,
                              'mybadges': my_badges,
                              }, context_instance=RequestContext(request))

def badge(request, id):
    badge = get_object_or_404(Badge, id=id)
    awards = Award.objects.extra(
                                 select={'id': 'auth_user.id',
                                 'name': 'auth_user.username',
                                 'rep':'auth_user.reputation',
                                 'gold': 'auth_user.gold',
                                 'silver': 'auth_user.silver',
                                 'bronze': 'auth_user.bronze'},
                                 tables=['award', 'auth_user'],
                                 where=['badge_id=%s AND user_id=auth_user.id'],
                                 params=[id]
                                 ).distinct('auth_user.id')
    return render_to_response('badge.html', {
                              'awards': awards,
                              'badge': badge,
                              }, context_instance=RequestContext(request))

def read_message(request):
    if request.method == "POST":
        if request.POST['formdata'] == 'required':
            request.session['message_silent'] = 1
            if request.user.is_authenticated():
                request.user.delete_messages()
    return HttpResponse('')

def upload(request):
    class FileTypeNotAllow(Exception):
        pass
    class FileSizeNotAllow(Exception):
        pass
    class UploadPermissionNotAuthorized(Exception):
        pass

    #<result><msg><![CDATA[%s]]></msg><error><![CDATA[%s]]></error><file_url>%s</file_url></result>
    xml_template = "<result><msg><![CDATA[%s]]></msg><error><![CDATA[%s]]></error><file_url>%s</file_url></result>"

    try:
        f = request.FILES['file-upload']
        # check upload permission
        if not can_upload_files(request.user):
            raise UploadPermissionNotAuthorized

        # check file type
        file_name_suffix = os.path.splitext(f.name)[1].lower()
        if not file_name_suffix in settings.ALLOW_FILE_TYPES:
            raise FileTypeNotAllow

        # genetate new file name
        new_file_name = str(time.time()).replace('.', str(random.randint(0, 100000))) + file_name_suffix
        # use default storage to store file
        default_storage.save(new_file_name, f)
        # check file size
        # byte
        size = default_storage.size(new_file_name)
        if size > settings.ALLOW_MAX_FILE_SIZE:
            default_storage.delete(new_file_name)
            raise FileSizeNotAllow

        result = xml_template % ('Good', '', default_storage.url(new_file_name))
    except UploadPermissionNotAuthorized:
        result = xml_template % ('', _('uploading images is limited to users with >60 reputation points'), '')
    except FileTypeNotAllow:
        result = xml_template % ('', _("allowed file types are 'jpg', 'jpeg', 'gif', 'bmp', 'png', 'tiff'"), '')
    except FileSizeNotAllow:
        result = xml_template % ('', _("maximum upload file size is %sK") % settings.ALLOW_MAX_FILE_SIZE / 1024, '')
    except Exception:
        result = xml_template % ('', _('Error uploading file. Please contact the site administrator. Thank you. %s' % Exception), '')

    return HttpResponse(result, mimetype="application/xml")

def books(request):
    return HttpResponseRedirect("/books/mysql-zhaoyang")
    
def book(request, short_name, unanswered=False):
    """
    1. questions list
    2. book info
    3. author info and blog rss items
    """
    """
    List of Questions, Tagged questions, and Unanswered questions.
    """
    books = Book.objects.extra(where=['short_name = %s'], params=[short_name])
    match_count = len(books)
    if match_count == 0:
        raise Http404
    else:
        # the book info
        book = books[0]
        # get author info
        author_info = BookAuthorInfo.objects.get(book=book)
        # get author rss info
        author_rss = BookAuthorRss.objects.filter(book=book)

        # get pagesize from session, if failed then get default value
        user_page_size = request.session.get("pagesize", QUESTIONS_PAGE_SIZE)
        # set pagesize equal to logon user specified value in database
        if request.user.is_authenticated() and request.user.questions_per_page > 0:
            user_page_size = request.user.questions_per_page
            
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        view_id = request.GET.get('sort', None)
        view_dic = {"latest":"-added_at", "active":"-last_activity_at", "hottest":"-answer_count", "mostvoted":"-score"}
        try:
            orderby = view_dic[view_id]
        except KeyError:
            view_id = "latest"
            orderby = "-added_at"
            
        # check if request is from tagged questions
        if unanswered:
            # check if request is from unanswered questions
            # Article.objects.filter(publications__id__exact=1)
            objects = Question.objects.filter(book__id__exact=book.id, deleted=False, answer_count=0).order_by(orderby)
        else:
            objects = Question.objects.filter(book__id__exact=book.id, deleted=False).order_by(orderby)

        # RISK - inner join queries
        objects = objects.select_related();
        objects_list = Paginator(objects, user_page_size)
        questions = objects_list.page(page)

        return render_to_response('book.html', {
                                  "book": book,
                                  "author_info": author_info,
                                  "author_rss": author_rss,
                                  "questions": questions,
                                  "context": {
                                  'is_paginated': True,
                                  'pages': objects_list.num_pages,
                                  'page': page,
                                  'has_previous': questions.has_previous(),
                                  'has_next': questions.has_next(),
                                  'previous': questions.previous_page_number(),
                                  'next': questions.next_page_number(),
                                  'base_url': request.path + '?sort=%s&' % view_id,
                                  'pagesize': user_page_size
                                  }
                                  }, context_instance=RequestContext(request))

@login_required
def ask_book(request, short_name):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            added_at = datetime.datetime.now()
            html = sanitize_html(markdowner.convert(form.cleaned_data['text']))
            question = Question(
                                title=strip_tags(form.cleaned_data['title']),
                                author=request.user,
                                added_at=added_at,
                                last_activity_at=added_at,
                                last_activity_by=request.user,
                                wiki=form.cleaned_data['wiki'],
                                tagnames=form.cleaned_data['tags'].strip(),
                                html=html,
                                summary=strip_tags(html)[:120]
                                )
            if question.wiki:
                question.last_edited_by = question.author
                question.last_edited_at = added_at
                question.wikified_at = added_at

            question.save()

            # create the first revision
            QuestionRevision.objects.create(
                                            question=question,
                                            revision=1,
                                            title=question.title,
                                            author=request.user,
                                            revised_at=added_at,
                                            tagnames=question.tagnames,
                                            summary=CONST['default_version'],
                                            text=form.cleaned_data['text']
                                            )
            
            books = Book.objects.extra(where=['short_name = %s'], params=[short_name])
            match_count = len(books)
            if match_count == 1:
                # the book info
                book = books[0]
                book.questions.add(question)

            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AskForm()

    tags = _get_tags_cache_json()
    return render_to_response('ask.html', {
                              'form': form,
                              'tags': tags,
                              }, context_instance=RequestContext(request))

def search(request):
    """
    Search by question, user and tag keywords.
    For questions now we only search keywords in question title.
    """
    if request.method == "GET":
        keywords = request.GET.get("q")
        search_type = request.GET.get("t")
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        if keywords is None:
            return HttpResponseRedirect('/')
        if search_type == 'tag':
            return HttpResponseRedirect('/tags/?q=%s&page=%s' % (keywords.strip(), page))
        elif search_type == "user":
            return HttpResponseRedirect('/users/?q=%s&page=%s' % (keywords.strip(), page))
        elif search_type == "question":
            
            template_file = "questions.html"
            # Set flag to False by default. If it is equal to True, then need to be saved.
            pagesize_changed = False
            # get pagesize from session, if failed then get default value
            user_page_size = request.session.get("pagesize", QUESTIONS_PAGE_SIZE)
            # set pagesize equal to logon user specified value in database
            if request.user.is_authenticated() and request.user.questions_per_page > 0:
                user_page_size = request.user.questions_per_page

            try:
                page = int(request.GET.get('page', '1'))
                # get new pagesize from UI selection
                pagesize = int(request.GET.get('pagesize', user_page_size))
                if pagesize <> user_page_size:
                    pagesize_changed = True

            except ValueError:
                page = 1
                pagesize  = user_page_size

            # save this pagesize to user database
            if pagesize_changed:
                request.session["pagesize"] = pagesize
                if request.user.is_authenticated():
                    user = request.user
                    user.questions_per_page = pagesize
                    user.save()

            view_id = request.GET.get('sort', None)
            view_dic = {"latest":"-added_at", "active":"-last_activity_at", "hottest":"-answer_count", "mostvoted":"-score"}
            try:
                orderby = view_dic[view_id]
            except KeyError:
                view_id = "latest"
                orderby = "-added_at"
                
            objects = Question.objects.filter(deleted=False).extra(where=['title like %s'], params=['%' + keywords + '%']).order_by(orderby)

            # RISK - inner join queries
            objects = objects.select_related();
            objects_list = Paginator(objects, pagesize)
            questions = objects_list.page(page)

            # Get related tags from this page objects
            related_tags = []
            for question in questions.object_list:
                tags = list(question.tags.all())
                for tag in tags:
                    if tag not in related_tags:
                        related_tags.append(tag)

            return render_to_response(template_file, {
                                      "questions": questions,
                                      "tab_id": view_id,
                                      "questions_count": objects_list.count,
                                      "tags": related_tags,
                                      "searchtag": None,
                                      "searchtitle": keywords,
                                      "keywords": keywords,
                                      "is_unanswered": False,
                                      "context": {
                                      'is_paginated': True,
                                      'pages': objects_list.num_pages,
                                      'page': page,
                                      'has_previous': questions.has_previous(),
                                      'has_next': questions.has_next(),
                                      'previous': questions.previous_page_number(),
                                      'next': questions.next_page_number(),
                                      'base_url': request.path + '?t=question&q=%s&sort=%s&' % (keywords, view_id),
                                      'pagesize': pagesize
                                      }}, context_instance=RequestContext(request))
 
    else:
        raise Http404

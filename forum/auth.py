"""
Authorisation related functions.

The actions a User is authorised to perform are dependent on their reputation
and superuser status.
"""
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from models import Repute
from models import Question
from models import Answer
from const import TYPE_REPUTATION
question_type = ContentType.objects.get_for_model(Question)
answer_type = ContentType.objects.get_for_model(Answer)

VOTE_UP                   = 15
FLAG_OFFENSIVE            = 15
POST_IMAGES               = 15
LEAVE_COMMENTS            = 50
UPLOAD_FILES              = 60
VOTE_DOWN                 = 100
CLOSE_OWN_QUESTIONS       = 250
RETAG_OTHER_QUESTIONS     = 500
REOPEN_OWN_QUESTIONS      = 500
EDIT_COMMUNITY_WIKI_POSTS = 750
EDIT_OTHER_POSTS          = 2000
DELETE_COMMENTS           = 2000
VIEW_OFFENSIVE_FLAGS      = 2000
DISABLE_URL_NOFOLLOW      = 2000
CLOSE_OTHER_QUESTIONS     = 3000
LOCK_POSTS                = 4000

VOTE_RULES = {
    'scope_votes_per_user_per_day' : 30, # how many votes of one user has everyday
    'scope_flags_per_user_per_day' : 5,  # how many times user can flag posts everyday
    'scope_warn_votes_left' : 10,        # start when to warn user how many votes left
    'scope_deny_unvote_days' : 1,        # if 1 days passed, user can't cancel votes.
    'scope_flags_invisible_main_page' : 3, # post doesn't show on main page if has more than 3 offensive flags
    'scope_flags_delete_post' : 5,         # post will be deleted if it has more than 5 offensive flags
}

REPUTATION_RULES = {
    'initial_score'                       : 1,
    'scope_per_day_by_upvotes'            : 200,
    'gain_by_upvoted'                     : 10,
    'gain_by_answer_accepted'             : 15,
    'gain_by_accepting_answer'            : 2,
    'gain_by_downvote_canceled'           : 2,
    'gain_by_canceling_downvote'          : 1,
    'lose_by_canceling_accepted_answer'   : -2,
    'lose_by_accepted_answer_cancled'     : -15,
    'lose_by_downvoted'                   : -2,
    'lose_by_flagged'                     : -2,
    'lose_by_downvoting'                  : -1,
    'lose_by_flagged_lastrevision_3_times': -30,
    'lose_by_flagged_lastrevision_5_times': -100,
    'lose_by_upvote_canceled'             : -10,
}

def can_vote_up(user):
    """Determines if a User can vote Questions and Answers up."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_UP or
        user.is_superuser)

def can_flag_offensive(user):
    """Determines if a User can flag Questions and Answers as offensive."""
    return user.is_authenticated() and (
        user.reputation >= FLAG_OFFENSIVE or
        user.is_superuser)

def can_add_comments(user):
    """Determines if a User can add comments to Questions and Answers."""
    return user.is_authenticated() and (
        user.reputation >= LEAVE_COMMENTS or
        user.is_superuser)

def can_vote_down(user):
    """Determines if a User can vote Questions and Answers down."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_DOWN or
        user.is_superuser)

def can_retag_questions(user):
    """Determines if a User can retag Questions."""
    return user.is_authenticated() and (
        RETAG_OTHER_QUESTIONS <= user.reputation < EDIT_OTHER_POSTS or
        user.is_superuser)

def can_edit_post(user, post):
    """Determines if a User can edit the given Question or Answer."""
    return user.is_authenticated() and (
        user.id == post.author_id or
        (post.wiki and user.reputation >= EDIT_COMMUNITY_WIKI_POSTS) or
        user.reputation >= EDIT_OTHER_POSTS or
        user.is_superuser)

def can_delete_comment(user, comment):
    """Determines if a User can delete the given Comment."""
    return user.is_authenticated() and (
        user.id == comment.user_id or
        user.reputation >= DELETE_COMMENTS or
        user.is_superuser)

def can_view_offensive_flags(user):
    """Determines if a User can view offensive flag counts."""
    return user.is_authenticated() and (
        user.reputation >= VIEW_OFFENSIVE_FLAGS or
        user.is_superuser)

def can_close_question(user, question):
    """Determines if a User can close the given Question."""
    return user.is_authenticated() and (
        (user.id == question.author_id and
         user.reputation >= CLOSE_OWN_QUESTIONS) or
        user.reputation >= CLOSE_OTHER_QUESTIONS or
        user.is_superuser)

def can_lock_posts(user):
    """Determines if a User can lock Questions or Answers."""
    return user.is_authenticated() and (
        user.reputation >= LOCK_POSTS or
        user.is_superuser)

def can_follow_url(user):
    """Determines if the URL link can be followed by Google search engine."""
    return user.reputation >= DISABLE_URL_NOFOLLOW

def can_accept_answer(user, question, answer):
    return (user.is_authenticated() and
        question.author != answer.author and
        question.author == user) or user.is_superuser

# now only support to reopen own question except superuser
def can_reopen_question(user, question):
    return (user.is_authenticated() and
        user.id == question.author_id and
        user.reputation >= REOPEN_OWN_QUESTIONS) or user.is_superuser

def can_delete_post(user, post):
    return (user.is_authenticated() and
        user.id == post.author_id) or user.is_superuser

def can_view_deleted_post(user, post):
    return user.is_superuser

# user preferences view permissions
def is_user_self(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)
    
def can_view_user_votes(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_view_user_preferences(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_view_user_edit(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_upload_files(request_user):
    return (request_user.is_authenticated() and request_user.reputation >= UPLOAD_FILES) or \
           request_user.is_superuser

###########################################
## actions and reputation changes event
###########################################
def calculate_reputation(origin, offset):
    result = int(origin) + int(offset)
    if (result > 0):
        return result
    else: 
        return 1

@transaction.commit_on_success
def onFlaggedItem(item, post, user):

    item.save()
    post.offensive_flag_count = post.offensive_flag_count + 1
    post.save()

    post.author.reputation = calculate_reputation(post.author.reputation,
                           int(REPUTATION_RULES['lose_by_flagged']))
    post.author.save()

    question = post
    if ContentType.objects.get_for_model(post) == answer_type:
        question = post.question

    reputation = Repute(user=post.author,
               negative=int(REPUTATION_RULES['lose_by_flagged']),
               question=question, reputed_at=datetime.datetime.now(),
               reputation_type=-4,
               reputation=post.author.reputation)
    reputation.save()

    #todo: These should be updated to work on same revisions.
    if post.offensive_flag_count ==  VOTE_RULES['scope_flags_invisible_main_page'] :
        post.author.reputation = calculate_reputation(post.author.reputation,
                               int(REPUTATION_RULES['lose_by_flagged_lastrevision_3_times']))
        post.author.save()

        reputation = Repute(user=post.author,
                   negative=int(REPUTATION_RULES['lose_by_flagged_lastrevision_3_times']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-6,
                   reputation=post.author.reputation)
        reputation.save()

    elif post.offensive_flag_count == VOTE_RULES['scope_flags_delete_post']:
        post.author.reputation = calculate_reputation(post.author.reputation,
                               int(REPUTATION_RULES['lose_by_flagged_lastrevision_5_times']))
        post.author.save()

        reputation = Repute(user=post.author,
                   negative=int(REPUTATION_RULES['lose_by_flagged_lastrevision_5_times']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-7,
                   reputation=post.author.reputation)
        reputation.save()

        post.deleted = True
        #post.deleted_at = datetime.datetime.now()
        #post.deleted_by = Admin
        post.save()


@transaction.commit_on_success
def onAnswerAccept(answer, user):
    answer.accepted = True
    answer.accepted_at = datetime.datetime.now()
    answer.question.answer_accepted = True
    answer.save()
    answer.question.save()

    answer.author.reputation = calculate_reputation(answer.author.reputation,
                             int(REPUTATION_RULES['gain_by_answer_accepted']))
    answer.author.save()
    reputation = Repute(user=answer.author,
               positive=int(REPUTATION_RULES['gain_by_answer_accepted']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=2,
               reputation=answer.author.reputation)
    reputation.save()

    user.reputation = calculate_reputation(user.reputation,
                    int(REPUTATION_RULES['gain_by_accepting_answer']))
    user.save()
    reputation = Repute(user=user,
               positive=int(REPUTATION_RULES['gain_by_accepting_answer']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=3,
               reputation=user.reputation)
    reputation.save()

@transaction.commit_on_success
def onAnswerAcceptCanceled(answer, user):
    answer.accepted = False
    answer.accepted_at = None
    answer.question.answer_accepted = False
    answer.save()
    answer.question.save()

    answer.author.reputation = calculate_reputation(answer.author.reputation,
                             int(REPUTATION_RULES['lose_by_accepted_answer_cancled']))
    answer.author.save()
    reputation = Repute(user=answer.author,
               negative=int(REPUTATION_RULES['lose_by_accepted_answer_cancled']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=-2,
               reputation=answer.author.reputation)
    reputation.save()

    user.reputation = calculate_reputation(user.reputation,
                    int(REPUTATION_RULES['lose_by_canceling_accepted_answer']))
    user.save()
    reputation = Repute(user=user,
               negative=int(REPUTATION_RULES['lose_by_canceling_accepted_answer']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=-1,
               reputation=user.reputation)
    reputation.save()

@transaction.commit_on_success
def onUpVoted(vote, post, user):
    vote.save()

    post.vote_up_count = int(post.vote_up_count) + 1
    post.score = int(post.score) + 1
    post.save()

    if not post.wiki:
        author = post.author
        if Repute.objects.get_reputation_by_upvoted_today(author) <  int(REPUTATION_RULES['scope_per_day_by_upvotes']):
            author.reputation = calculate_reputation(author.reputation,
                              int(REPUTATION_RULES['gain_by_upvoted']))
            author.save()

            question = post
            if ContentType.objects.get_for_model(post) == answer_type:
                question = post.question

            reputation = Repute(user=author,
                       positive=int(REPUTATION_RULES['gain_by_upvoted']),
                       question=question,
                       reputed_at=datetime.datetime.now(),
                       reputation_type=1,
                       reputation=author.reputation)
            reputation.save()

@transaction.commit_on_success
def onUpVotedCanceled(vote, post, user):
    vote.delete()

    post.vote_up_count = int(post.vote_up_count) - 1
    if post.vote_up_count < 0:
        post.vote_up_count  = 0
    post.score = int(post.score) - 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['lose_by_upvote_canceled']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   negative=int(REPUTATION_RULES['lose_by_upvote_canceled']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-8,
                   reputation=author.reputation)
        reputation.save()

@transaction.commit_on_success
def onDownVoted(vote, post, user):
    vote.save()

    post.vote_down_count = int(post.vote_down_count) + 1
    post.score = int(post.score) - 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['lose_by_downvoted']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   negative=int(REPUTATION_RULES['lose_by_downvoted']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-3,
                   reputation=author.reputation)
        reputation.save()

        user.reputation = calculate_reputation(user.reputation,
                        int(REPUTATION_RULES['lose_by_downvoting']))
        user.save()

        reputation = Repute(user=user,
                   negative=int(REPUTATION_RULES['lose_by_downvoting']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-5,
                   reputation=user.reputation)
        reputation.save()

@transaction.commit_on_success
def onDownVotedCanceled(vote, post, user):
    vote.delete()

    post.vote_down_count = int(post.vote_down_count) - 1
    if post.vote_down_count < 0:
        post.vote_down_count  = 0
    post.score = post.score + 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['gain_by_downvote_canceled']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   positive=int(REPUTATION_RULES['gain_by_downvote_canceled']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=4,
                   reputation=author.reputation)
        reputation.save()

        user.reputation = calculate_reputation(user.reputation,
                        int(REPUTATION_RULES['gain_by_canceling_downvote']))
        user.save()

        reputation = Repute(user=user,
                   positive=int(REPUTATION_RULES['gain_by_canceling_downvote']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=5,
                   reputation=user.reputation)
        reputation.save()

def onDeleteCanceled(post, user):
    post.deleted = False
    post.deleted_by = None
    post.deleted_at = None
    post.save()
    for tag in list(post.tags.all()):
        if tag.used_count == 1 and tag.deleted:
            tag.deleted = False
            tag.deleted_by = None
            tag.deleted_at = None
            tag.save()

def onDeleted(post, user):
    post.deleted = True
    post.deleted_by = user
    post.deleted_at = datetime.datetime.now()
    post.save()

    for tag in list(post.tags.all()):
        if tag.used_count == 1:
            tag.deleted = True
            tag.deleted_by = user
            tag.deleted_at = datetime.datetime.now()
            tag.save()
=======
﻿"""
Authorisation related functions.

The actions a User is authorised to perform are dependent on their reputation
and superuser status.
"""
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from models import Repute
from models import Question
from models import Answer
from const import TYPE_REPUTATION
question_type = ContentType.objects.get_for_model(Question)
answer_type = ContentType.objects.get_for_model(Answer)

VOTE_UP                   = 15
FLAG_OFFENSIVE            = 15
POST_IMAGES               = 15
LEAVE_COMMENTS            = 50
UPLOAD_FILES              = 60
VOTE_DOWN                 = 100
CLOSE_OWN_QUESTIONS       = 250
RETAG_OTHER_QUESTIONS     = 500
REOPEN_OWN_QUESTIONS      = 500
EDIT_COMMUNITY_WIKI_POSTS = 750
EDIT_OTHER_POSTS          = 2000
DELETE_COMMENTS           = 2000
VIEW_OFFENSIVE_FLAGS      = 2000
DISABLE_URL_NOFOLLOW      = 2000
CLOSE_OTHER_QUESTIONS     = 3000
LOCK_POSTS                = 4000

VOTE_RULES = {
    'scope_votes_per_user_per_day' : 30, # how many votes of one user has everyday
    'scope_flags_per_user_per_day' : 5,  # how many times user can flag posts everyday
    'scope_warn_votes_left' : 10,        # start when to warn user how many votes left
    'scope_deny_unvote_days' : 1,        # if 1 days passed, user can't cancel votes.
    'scope_flags_invisible_main_page' : 3, # post doesn't show on main page if has more than 3 offensive flags
    'scope_flags_delete_post' : 5,         # post will be deleted if it has more than 5 offensive flags
}

REPUTATION_RULES = {
    'initial_score'                       : 1,
    'scope_per_day_by_upvotes'            : 200,
    'gain_by_upvoted'                     : 10,
    'gain_by_answer_accepted'             : 15,
    'gain_by_accepting_answer'            : 2,
    'gain_by_downvote_canceled'           : 2,
    'gain_by_canceling_downvote'          : 1,
    'lose_by_canceling_accepted_answer'   : -2,
    'lose_by_accepted_answer_cancled'     : -15,
    'lose_by_downvoted'                   : -2,
    'lose_by_flagged'                     : -2,
    'lose_by_downvoting'                  : -1,
    'lose_by_flagged_lastrevision_3_times': -30,
    'lose_by_flagged_lastrevision_5_times': -100,
    'lose_by_upvote_canceled'             : -10,
}

def can_vote_up(user):
    """Determines if a User can vote Questions and Answers up."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_UP or
        user.is_superuser)

def can_flag_offensive(user):
    """Determines if a User can flag Questions and Answers as offensive."""
    return user.is_authenticated() and (
        user.reputation >= FLAG_OFFENSIVE or
        user.is_superuser)

def can_add_comments(user):
    """Determines if a User can add comments to Questions and Answers."""
    return user.is_authenticated() and (
        user.reputation >= LEAVE_COMMENTS or
        user.is_superuser)

def can_vote_down(user):
    """Determines if a User can vote Questions and Answers down."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_DOWN or
        user.is_superuser)

def can_retag_questions(user):
    """Determines if a User can retag Questions."""
    return user.is_authenticated() and (
        RETAG_OTHER_QUESTIONS <= user.reputation < EDIT_OTHER_POSTS or
        user.is_superuser)

def can_edit_post(user, post):
    """Determines if a User can edit the given Question or Answer."""
    return user.is_authenticated() and (
        user.id == post.author_id or
        (post.wiki and user.reputation >= EDIT_COMMUNITY_WIKI_POSTS) or
        user.reputation >= EDIT_OTHER_POSTS or
        user.is_superuser)

def can_delete_comment(user, comment):
    """Determines if a User can delete the given Comment."""
    return user.is_authenticated() and (
        user.id == comment.user_id or
        user.reputation >= DELETE_COMMENTS or
        user.is_superuser)

def can_view_offensive_flags(user):
    """Determines if a User can view offensive flag counts."""
    return user.is_authenticated() and (
        user.reputation >= VIEW_OFFENSIVE_FLAGS or
        user.is_superuser)

def can_close_question(user, question):
    """Determines if a User can close the given Question."""
    return user.is_authenticated() and (
        (user.id == question.author_id and
         user.reputation >= CLOSE_OWN_QUESTIONS) or
        user.reputation >= CLOSE_OTHER_QUESTIONS or
        user.is_superuser)

def can_lock_posts(user):
    """Determines if a User can lock Questions or Answers."""
    return user.is_authenticated() and (
        user.reputation >= LOCK_POSTS or
        user.is_superuser)

def can_follow_url(user):
    """Determines if the URL link can be followed by Google search engine."""
    return user.reputation >= DISABLE_URL_NOFOLLOW

def can_accept_answer(user, question, answer):
    return (user.is_authenticated() and
        question.author != answer.author and
        question.author == user) or user.is_superuser

# now only support to reopen own question except superuser
def can_reopen_question(user, question):
    return (user.is_authenticated() and
        user.id == question.author_id and
        user.reputation >= REOPEN_OWN_QUESTIONS) or user.is_superuser

def can_delete_post(user, post):
    return (user.is_authenticated() and
        user.id == post.author_id) or user.is_superuser

def can_view_deleted_post(user, post):
    return user.is_superuser

# user preferences view permissions
def is_user_self(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)
    
def can_view_user_votes(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_view_user_preferences(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_view_user_edit(request_user, target_user):
    return (request_user.is_authenticated() and request_user == target_user)

def can_upload_files(request_user):
    return (request_user.is_authenticated() and request_user.reputation >= UPLOAD_FILES) or \
           request_user.is_superuser

###########################################
## actions and reputation changes event
###########################################
def calculate_reputation(origin, offset):
    result = int(origin) + int(offset)
    return result if result > 0 else 1

@transaction.commit_on_success
def onFlaggedItem(item, post, user):

    item.save()
    post.offensive_flag_count = post.offensive_flag_count + 1
    post.save()

    post.author.reputation = calculate_reputation(post.author.reputation,
                           int(REPUTATION_RULES['lose_by_flagged']))
    post.author.save()

    question = post
    if ContentType.objects.get_for_model(post) == answer_type:
        question = post.question

    reputation = Repute(user=post.author,
               negative=int(REPUTATION_RULES['lose_by_flagged']),
               question=question, reputed_at=datetime.datetime.now(),
               reputation_type=-4,
               reputation=post.author.reputation)
    reputation.save()

    #todo: These should be updated to work on same revisions.
    if post.offensive_flag_count ==  VOTE_RULES['scope_flags_invisible_main_page'] :
        post.author.reputation = calculate_reputation(post.author.reputation,
                               int(REPUTATION_RULES['lose_by_flagged_lastrevision_3_times']))
        post.author.save()

        reputation = Repute(user=post.author,
                   negative=int(REPUTATION_RULES['lose_by_flagged_lastrevision_3_times']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-6,
                   reputation=post.author.reputation)
        reputation.save()

    elif post.offensive_flag_count == VOTE_RULES['scope_flags_delete_post']:
        post.author.reputation = calculate_reputation(post.author.reputation,
                               int(REPUTATION_RULES['lose_by_flagged_lastrevision_5_times']))
        post.author.save()

        reputation = Repute(user=post.author,
                   negative=int(REPUTATION_RULES['lose_by_flagged_lastrevision_5_times']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-7,
                   reputation=post.author.reputation)
        reputation.save()

        post.deleted = True
        #post.deleted_at = datetime.datetime.now()
        #post.deleted_by = Admin
        post.save()


@transaction.commit_on_success
def onAnswerAccept(answer, user):
    answer.accepted = True
    answer.accepted_at = datetime.datetime.now()
    answer.question.answer_accepted = True
    answer.save()
    answer.question.save()

    answer.author.reputation = calculate_reputation(answer.author.reputation,
                             int(REPUTATION_RULES['gain_by_answer_accepted']))
    answer.author.save()
    reputation = Repute(user=answer.author,
               positive=int(REPUTATION_RULES['gain_by_answer_accepted']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=2,
               reputation=answer.author.reputation)
    reputation.save()

    user.reputation = calculate_reputation(user.reputation,
                    int(REPUTATION_RULES['gain_by_accepting_answer']))
    user.save()
    reputation = Repute(user=user,
               positive=int(REPUTATION_RULES['gain_by_accepting_answer']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=3,
               reputation=user.reputation)
    reputation.save()

@transaction.commit_on_success
def onAnswerAcceptCanceled(answer, user):
    answer.accepted = False
    answer.accepted_at = None
    answer.question.answer_accepted = False
    answer.save()
    answer.question.save()

    answer.author.reputation = calculate_reputation(answer.author.reputation,
                             int(REPUTATION_RULES['lose_by_accepted_answer_cancled']))
    answer.author.save()
    reputation = Repute(user=answer.author,
               negative=int(REPUTATION_RULES['lose_by_accepted_answer_cancled']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=-2,
               reputation=answer.author.reputation)
    reputation.save()

    user.reputation = calculate_reputation(user.reputation,
                    int(REPUTATION_RULES['lose_by_canceling_accepted_answer']))
    user.save()
    reputation = Repute(user=user,
               negative=int(REPUTATION_RULES['lose_by_canceling_accepted_answer']),
               question=answer.question,
               reputed_at=datetime.datetime.now(),
               reputation_type=-1,
               reputation=user.reputation)
    reputation.save()

@transaction.commit_on_success
def onUpVoted(vote, post, user):
    vote.save()

    post.vote_up_count = int(post.vote_up_count) + 1
    post.score = int(post.score) + 1
    post.save()

    if not post.wiki:
        author = post.author
        if Repute.objects.get_reputation_by_upvoted_today(author) <  int(REPUTATION_RULES['scope_per_day_by_upvotes']):
            author.reputation = calculate_reputation(author.reputation,
                              int(REPUTATION_RULES['gain_by_upvoted']))
            author.save()

            question = post
            if ContentType.objects.get_for_model(post) == answer_type:
                question = post.question

            reputation = Repute(user=author,
                       positive=int(REPUTATION_RULES['gain_by_upvoted']),
                       question=question,
                       reputed_at=datetime.datetime.now(),
                       reputation_type=1,
                       reputation=author.reputation)
            reputation.save()

@transaction.commit_on_success
def onUpVotedCanceled(vote, post, user):
    vote.delete()

    post.vote_up_count = int(post.vote_up_count) - 1
    if post.vote_up_count < 0:
        post.vote_up_count  = 0
    post.score = int(post.score) - 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['lose_by_upvote_canceled']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   negative=int(REPUTATION_RULES['lose_by_upvote_canceled']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-8,
                   reputation=author.reputation)
        reputation.save()

@transaction.commit_on_success
def onDownVoted(vote, post, user):
    vote.save()

    post.vote_down_count = int(post.vote_down_count) + 1
    post.score = int(post.score) - 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['lose_by_downvoted']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   negative=int(REPUTATION_RULES['lose_by_downvoted']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-3,
                   reputation=author.reputation)
        reputation.save()

        user.reputation = calculate_reputation(user.reputation,
                        int(REPUTATION_RULES['lose_by_downvoting']))
        user.save()

        reputation = Repute(user=user,
                   negative=int(REPUTATION_RULES['lose_by_downvoting']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=-5,
                   reputation=user.reputation)
        reputation.save()

@transaction.commit_on_success
def onDownVotedCanceled(vote, post, user):
    vote.delete()

    post.vote_down_count = int(post.vote_down_count) - 1
    if post.vote_down_count < 0:
        post.vote_down_count  = 0
    post.score = post.score + 1
    post.save()

    if not post.wiki:
        author = post.author
        author.reputation = calculate_reputation(author.reputation,
                          int(REPUTATION_RULES['gain_by_downvote_canceled']))
        author.save()

        question = post
        if ContentType.objects.get_for_model(post) == answer_type:
            question = post.question

        reputation = Repute(user=author,
                   positive=int(REPUTATION_RULES['gain_by_downvote_canceled']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=4,
                   reputation=author.reputation)
        reputation.save()

        user.reputation = calculate_reputation(user.reputation,
                        int(REPUTATION_RULES['gain_by_canceling_downvote']))
        user.save()

        reputation = Repute(user=user,
                   positive=int(REPUTATION_RULES['gain_by_canceling_downvote']),
                   question=question,
                   reputed_at=datetime.datetime.now(),
                   reputation_type=5,
                   reputation=user.reputation)
        reputation.save()

def onDeleteCanceled(post, user):
    post.deleted = False
    post.deleted_by = None
    post.deleted_at = None
    post.save()
    for tag in list(post.tags.all()):
        if tag.used_count == 1 and tag.deleted:
            tag.deleted = False
            tag.deleted_by = None
            tag.deleted_at = None
            tag.save()

def onDeleted(post, user):
    post.deleted = True
    post.deleted_by = user
    post.deleted_at = datetime.datetime.now()
    post.save()

    for tag in list(post.tags.all()):
        if tag.used_count == 1:
            tag.deleted = True
            tag.deleted_by = user
            tag.deleted_at = datetime.datetime.now()
            tag.save()

# encoding:utf-8
from django.utils.translation import ugettext as _
"""
All constants could be used in other modules
For reasons that models, views can't have unicode text in this project, all unicode text go here.
"""
CLOSE_REASONS = (
    (1, _('duplicate question')),
    (2, _('question if off-topic or not relevant')),
    (3, _('too subjective and argumentative')),
    (4, _('is not an answer to the question')),
    (5, _('the question is answered, right answer was accepted')),
    (6, _('problem is not reproducible or outdated')),
    #(7, u'太局部、本地化的问题',)
    (7, _('question contains offensive inappropriate, or malicious remarks')),
    (8, _('spam or advertising')),
)

TYPE_REPUTATION = (
    (1, 'gain_by_upvoted'),
    (2, 'gain_by_answer_accepted'),
    (3, 'gain_by_accepting_answer'),
    (4, 'gain_by_downvote_canceled'),
    (5, 'gain_by_canceling_downvote'),
    (-1, 'lose_by_canceling_accepted_answer'),
    (-2, 'lose_by_accepted_answer_cancled'),
    (-3, 'lose_by_downvoted'),
    (-4, 'lose_by_flagged'),
    (-5, 'lose_by_downvoting'),
    (-6, 'lose_by_flagged_lastrevision_3_times'),
    (-7, 'lose_by_flagged_lastrevision_5_times'),
    (-8, 'lose_by_upvote_canceled'),
)

TYPE_ACTIVITY_ASK_QUESTION=1
TYPE_ACTIVITY_ANSWER=2
TYPE_ACTIVITY_COMMENT_QUESTION=3
TYPE_ACTIVITY_COMMENT_ANSWER=4
TYPE_ACTIVITY_UPDATE_QUESTION=5
TYPE_ACTIVITY_UPDATE_ANSWER=6
TYPE_ACTIVITY_PRIZE=7
TYPE_ACTIVITY_MARK_ANSWER=8
TYPE_ACTIVITY_VOTE_UP=9
TYPE_ACTIVITY_VOTE_DOWN=10
TYPE_ACTIVITY_CANCEL_VOTE=11
TYPE_ACTIVITY_DELETE_QUESTION=12
TYPE_ACTIVITY_DELETE_ANSWER=13
TYPE_ACTIVITY_MARK_OFFENSIVE=14
TYPE_ACTIVITY_UPDATE_TAGS=15
TYPE_ACTIVITY_FAVORITE=16
TYPE_ACTIVITY_USER_FULL_UPDATED = 17
#TYPE_ACTIVITY_EDIT_QUESTION=17
#TYPE_ACTIVITY_EDIT_ANSWER=18

TYPE_ACTIVITY = (
    (TYPE_ACTIVITY_ASK_QUESTION, _('question')),
    (TYPE_ACTIVITY_ANSWER, _('answer')),
    (TYPE_ACTIVITY_COMMENT_QUESTION, _('commented question')),
    (TYPE_ACTIVITY_COMMENT_ANSWER, _('commented answer')),
    (TYPE_ACTIVITY_UPDATE_QUESTION, _('edited question')),
    (TYPE_ACTIVITY_UPDATE_ANSWER, _('edited answer')),
    (TYPE_ACTIVITY_PRIZE, _('received award')),
    (TYPE_ACTIVITY_MARK_ANSWER, _('marked best answer')),
    (TYPE_ACTIVITY_VOTE_UP, _('upvoted')),
    (TYPE_ACTIVITY_VOTE_DOWN, _('downvoted')),
    (TYPE_ACTIVITY_CANCEL_VOTE, _('canceled vote')),
    (TYPE_ACTIVITY_DELETE_QUESTION, _('deleted question')),
    (TYPE_ACTIVITY_DELETE_ANSWER, _('deleted answer')),
    (TYPE_ACTIVITY_MARK_OFFENSIVE, _('marked offensive')),
    (TYPE_ACTIVITY_UPDATE_TAGS, _('updated tags')),
    (TYPE_ACTIVITY_FAVORITE, _('selected favorite')),
    (TYPE_ACTIVITY_USER_FULL_UPDATED, _('completed user profile')),
)

TYPE_RESPONSE = {
    'QUESTION_ANSWERED' : 'question_answered',
    'QUESTION_COMMENTED': 'question_commented',
    'ANSWER_COMMENTED'  : 'answer_commented',
    'ANSWER_ACCEPTED'   : 'answer_accepted',
}

CONST = {
    'closed'            : _('[closed]'),
	'deleted'           : _('[deleted]'),
    'default_version'   : _('initial version'),
    'retagged'          : _('retagged'),
}

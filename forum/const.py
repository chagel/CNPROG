# encoding:utf-8
"""
All constants could be used in other modules
For reasons that models, views can't have unicode text in this project, all unicode text go here.
"""
CLOSE_REASONS = (
    (1, u'完全重复的问题'),
    (2, u'不是编程技术问题'),
    (3, u'太主观性、引起争吵的问题'),
    (4, u'不是一个可以回答的“问题”'),
    (5, u'问题已经解决，已得到正确答案'),
    (6, u'已经过时、不可重现的问题'),
    (7, u'太局部、本地化的问题'),
    (8, u'恶意言论'),
    (9, u'垃圾广告'),
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
    (TYPE_ACTIVITY_ASK_QUESTION, u'提问'),
    (TYPE_ACTIVITY_ANSWER, u'回答'),
    (TYPE_ACTIVITY_COMMENT_QUESTION, u'评论问题'),
    (TYPE_ACTIVITY_COMMENT_ANSWER, u'评论回答'),
    (TYPE_ACTIVITY_UPDATE_QUESTION, u'修改问题'),
    (TYPE_ACTIVITY_UPDATE_ANSWER, u'修改回答'),
    (TYPE_ACTIVITY_PRIZE, u'获奖'),
    (TYPE_ACTIVITY_MARK_ANSWER, u'标记最佳答案'),
    (TYPE_ACTIVITY_VOTE_UP, u'投赞成票'),
    (TYPE_ACTIVITY_VOTE_DOWN, u'投反对票'),
    (TYPE_ACTIVITY_CANCEL_VOTE, u'撤销投票'),
    (TYPE_ACTIVITY_DELETE_QUESTION, u'删除问题'),
    (TYPE_ACTIVITY_DELETE_ANSWER, u'删除回答'),
    (TYPE_ACTIVITY_MARK_OFFENSIVE, u'标记垃圾帖'),
    (TYPE_ACTIVITY_UPDATE_TAGS, u'更新标签'),
    (TYPE_ACTIVITY_FAVORITE, u'收藏'),
    (TYPE_ACTIVITY_USER_FULL_UPDATED, u'完成个人所有资料'),
    #(TYPE_ACTIVITY_EDIT_QUESTION, u'编辑问题'),
    #(TYPE_ACTIVITY_EDIT_ANSWER, u'编辑答案'),
)

TYPE_RESPONSE = {
    'QUESTION_ANSWERED' : u'回答问题',
    'QUESTION_COMMENTED': u'问题评论',
    'ANSWER_COMMENTED'  : u'回答评论',
    'ANSWER_ACCEPTED'   : u'最佳答案',
}

CONST = {
    'closed'            : u' [已关闭]',
    'deleted'           : u' [已删除]',
    'default_version'   : u'初始版本',
    'retagged'          : u'更新了标签',

}

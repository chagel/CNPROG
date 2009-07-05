#!/usr/bin/env python
#encoding:utf-8
#-------------------------------------------------------------------------------
# Name:        Award badges command
# Purpose:     This is a command file croning in background process regularly to
#              query database and award badges for user's special acitivities.
#
# Author:      Mike, Sailing
#
# Created:     18/01/2009
# Copyright:   (c) Mike 2009
# Licence:     GPL V2
#-------------------------------------------------------------------------------

from datetime import datetime, date
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from forum.models import *
from forum.const import *
from base_command import BaseCommand
"""
(1, '炼狱法师', 3, '炼狱法师', '删除自己有3个以上赞成票的帖子', 1, 0),
(2, '压力白领', 3, '压力白领', '删除自己有3个以上反对票的帖子', 1, 0),
(3, '优秀回答', 3, '优秀回答', '回答好评10次以上', 1, 0),
(4, '优秀问题', 3, '优秀问题', '问题好评10次以上', 1, 0),
(5, '评论家', 3, '评论家', '评论10次以上', 0, 0),
(6, '流行问题', 3, '流行问题', '问题的浏览量超过1000人次', 1, 0),
(7, '巡逻兵', 3, '巡逻兵', '第一次标记垃圾帖子', 0, 0),
(8, '清洁工', 3, '清洁工', '第一次撤销投票', 0, 0),
(9, '批评家', 3, '批评家', '第一次反对票', 0, 0),
(10, '小编', 3, '小编', '第一次编辑更新', 0, 0),
(11, '村长', 3, '村长', '第一次重新标签', 0, 0),
(12, '学者', 3, '学者', '第一次标记答案', 0, 0),
(13, '学生', 3, '学生', '第一次提问并且有一次以上赞成票', 0, 0),
(14, '支持者', 3, '支持者', '第一次赞成票', 0, 0),
(15, '教师', 3, '教师', '第一次回答问题并且得到一个以上赞成票', 0, 0),
(16, '自传作者', 3, '自传作者', '完整填写用户资料所有选项', 0, 0),
(17, '自学成才', 3, '自学成才', '回答自己的问题并且有3个以上赞成票', 1, 0),
(18, '最有价值回答', 1, '最有价值回答', '回答超过100次赞成票', 1, 0),
(19, '最有价值问题', 1, '最有价值问题', '问题超过100次赞成票', 1, 0),
(20, '万人迷', 1, '万人迷', '问题被100人以上收藏', 1, 0),
(21, '著名问题', 1, '著名问题', '问题的浏览量超过10000人次', 1, 0),
(22, 'alpha用户', 2, 'alpha用户', '内测期间的活跃用户', 0, 0),
(23, '极好回答', 2, '极好回答', '回答超过25次赞成票', 1, 0),
(24, '极好问题', 2, '极好问题', '问题超过25次赞成票', 1, 0),
(25, '受欢迎问题', 2, '受欢迎问题', '问题被25人以上收藏', 1, 0),
(26, '优秀市民', 2, '优秀市民', '投票300次以上', 0, 0),
(27, '编辑主任', 2, '编辑主任', '编辑了100个帖子', 0, 0),
(28, '通才', 2, '通才', '在多个标签领域活跃', 0, 0),
(29, '专家', 2, '专家', '在一个标签领域活跃出众', 0, 0),
(30, '老鸟', 2, '老鸟', '活跃超过一年的用户', 0, 0),
(31, '最受关注问题', 2, '最受关注问题', '问题的浏览量超过2500人次', 1, 0),
(32, '学问家', 2, '学问家', '第一次回答被投赞成票10次以上', 0, 0),
(33, 'beta用户', 2, 'beta用户', 'beta期间活跃参与', 0, 0),
(34, '导师', 2, '导师', '被指定为最佳答案并且赞成票40以上', 1, 0),
(35, '巫师', 2, '巫师', '在提问60天之后回答并且赞成票5次以上', 1, 0),
(36, '分类专家', 2, '分类专家', '创建的标签被50个以上问题使用', 1, 0);


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
"""

BADGE_AWARD_TYPE_FIRST = {
    TYPE_ACTIVITY_MARK_OFFENSIVE : 7,
    TYPE_ACTIVITY_CANCEL_VOTE: 8,
    TYPE_ACTIVITY_VOTE_DOWN : 9,
    TYPE_ACTIVITY_UPDATE_QUESTION : 10,
    TYPE_ACTIVITY_UPDATE_ANSWER : 10,
    TYPE_ACTIVITY_UPDATE_TAGS : 11,
    TYPE_ACTIVITY_MARK_ANSWER : 12,
    TYPE_ACTIVITY_VOTE_UP : 14,
    TYPE_ACTIVITY_USER_FULL_UPDATED: 16

}

class Command(BaseCommand):
    def handle_noargs(self, **options):
        try:
            self.alpha_user()
            self.beta_user()
            self.first_type_award()
            self.first_ask_be_voted()
            self.first_answer_be_voted()
            self.first_answer_be_voted_10()
            self.vote_count_300()
            self.edit_count_100()
            self.comment_count_10()
        except Exception, e:
            print e
        finally:
            connection.close()

    def alpha_user(self):
        """
        Before Jan 25, 2009(Chinese New Year Eve and enter into Beta for CNProg), every registered user
        will be awarded the "Alpha" badge if he has any activities.
        """
        alpha_end_date = date(2009, 1, 25)
        if date.today() < alpha_end_date:
            badge = get_object_or_404(Badge, id=22)
            for user in User.objects.all():
                award = Award.objects.filter(user=user, badge=badge)
                if award and not badge.multiple:
                    continue
                activities = Activity.objects.filter(user=user)
                if len(activities) > 0:
                    new_award = Award(user=user, badge=badge)
                    new_award.save()

    def beta_user(self):
        """
        Before Feb 25, 2009, every registered user
        will be awarded the "Beta" badge if he has any activities.
        """
        beta_end_date = date(2009, 2, 25)
        if date.today() < beta_end_date:
            badge = get_object_or_404(Badge, id=33)
            for user in User.objects.all():
                award = Award.objects.filter(user=user, badge=badge)
                if award and not badge.multiple:
                    continue
                activities = Activity.objects.filter(user=user)
                if len(activities) > 0:
                    new_award = Award(user=user, badge=badge)
                    new_award.save()

    def first_type_award(self):
        """
        This will award below badges for users first behaviors:

        (7, '巡逻兵', 3, '巡逻兵', '第一次标记垃圾帖子', 0, 0),
        (8, '清洁工', 3, '清洁工', '第一次撤销投票', 0, 0),
        (9, '批评家', 3, '批评家', '第一次反对票', 0, 0),
        (10, '小编', 3, '小编', '第一次编辑更新', 0, 0),
        (11, '村长', 3, '村长', '第一次重新标签', 0, 0),
        (12, '学者', 3, '学者', '第一次标记答案', 0, 0),
        (14, '支持者', 3, '支持者', '第一次赞成票', 0, 0),
        (16, '自传作者', 3, '自传作者', '完整填写用户资料所有选项', 0, 0),
        """
        activity_types = ','.join('%s' % item for item in BADGE_AWARD_TYPE_FIRST.keys())
        # ORDER BY user_id, activity_type
        query = "SELECT id, user_id, activity_type, content_type_id, object_id\
            FROM activity WHERE is_auditted = 0 AND activity_type IN (%s) ORDER BY user_id, activity_type" % activity_types

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            # collect activity_id in current process
            activity_ids = []
            last_user_id = 0
            last_activity_type = 0
            for row in rows:
                activity_ids.append(row[0])
                user_id = row[1]
                activity_type = row[2]
                content_type_id = row[3]
                object_id = row[4]

                # if the user and activity are same as the last, continue
                if user_id == last_user_id and activity_type == last_activity_type:
                    continue;

                user = get_object_or_404(User, id=user_id)
                badge = get_object_or_404(Badge, id=BADGE_AWARD_TYPE_FIRST[activity_type])
                content_type = get_object_or_404(ContentType, id=content_type_id)

                count = Award.objects.filter(user=user, badge=badge).count()
                if count and not badge.multiple:
                    continue
                else:
                    # new award
                    award = Award(user=user, badge=badge, content_type=content_type, object_id=object_id)
                    award.save()

                # set the current user_id and activity_type to last
                last_user_id = user_id
                last_activity_type = activity_type

            # update processed rows to auditted
            self.update_activities_auditted(cursor, activity_ids)
        finally:
            cursor.close()

    def first_ask_be_voted(self):
        """
        For user asked question and got first upvote, we award him following badge:

        (13, '学生', 3, '学生', '第一次提问并且有一次以上赞成票', 0, 0),
        """
        query = "SELECT act.user_id, q.vote_up_count, act.object_id FROM \
                    activity act, question q WHERE act.activity_type = %s AND \
                    act.object_id = q.id AND\
                    act.user_id NOT IN (SELECT distinct user_id FROM award WHERE badge_id = %s)" % (TYPE_ACTIVITY_ASK_QUESTION, 13)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            badge = get_object_or_404(Badge, id=13)
            content_type = ContentType.objects.get_for_model(Question)
            awarded_users = []
            for row in rows:
                user_id = row[0]
                vote_up_count = row[1]
                object_id = row[2]
                if vote_up_count > 0 and user_id not in awarded_users:
                    user = get_object_or_404(User, id=user_id)
                    award = Award(user=user, badge=badge, content_type=content_type, object_id=object_id)
                    award.save()
                    awarded_users.append(user_id)
        finally:
            cursor.close()

    def first_answer_be_voted(self):
        """
        When user answerd questions and got first upvote, we award him following badge:

        (15, '教师', 3, '教师', '第一次回答问题并且得到一个以上赞成票', 0, 0),
        """
        query = "SELECT act.user_id, a.vote_up_count, act.object_id FROM \
                    activity act, answer a WHERE act.activity_type = %s AND \
                    act.object_id = a.id AND\
                    act.user_id NOT IN (SELECT distinct user_id FROM award WHERE badge_id = %s)" % (TYPE_ACTIVITY_ANSWER, 15)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            awarded_users = []
            badge = get_object_or_404(Badge, id=15)
            content_type = ContentType.objects.get_for_model(Answer)
            for row in rows:
                user_id = row[0]
                vote_up_count = row[1]
                object_id = row[2]
                if vote_up_count > 0 and user_id not in awarded_users:
                    user = get_object_or_404(User, id=user_id)
                    award = Award(user=user, badge=badge, content_type=content_type, object_id=object_id)
                    award.save()
                    awarded_users.append(user_id)
        finally:
            cursor.close()

    def first_answer_be_voted_10(self):
        """
        (32, '学问家', 2, '学问家', '第一次回答被投赞成票10次以上', 0, 0)
        """
        query = "SELECT act.user_id, act.object_id FROM \
                    activity act, answer a WHERE act.object_id = a.id AND\
                    act.activity_type = %s AND \
                    a.vote_up_count >= 10 AND\
                    act.user_id NOT IN (SELECT user_id FROM award WHERE badge_id = %s)" % (TYPE_ACTIVITY_ANSWER, 32)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            awarded_users = []
            badge = get_object_or_404(Badge, id=32)
            content_type = ContentType.objects.get_for_model(Answer)
            for row in rows:
                user_id = row[0]
                if user_id not in awarded_users:
                    user = get_object_or_404(User, id=user_id)
                    object_id = row[1]
                    award = Award(user=user, badge=badge, content_type=content_type, object_id=object_id)
                    award.save()
                    awarded_users.append(user_id)
        finally:
            cursor.close()

    def vote_count_300(self):
        """
        (26, '优秀市民', 2, '优秀市民', '投票300次以上', 0, 0)
        """
        query = "SELECT count(*) vote_count, user_id FROM activity WHERE \
                    activity_type = %s OR \
                    activity_type = %s AND \
                    user_id NOT IN (SELECT user_id FROM award WHERE badge_id = %s) \
                    GROUP BY user_id HAVING vote_count >= 300" % (TYPE_ACTIVITY_VOTE_UP, TYPE_ACTIVITY_VOTE_DOWN, 26)

        self.__award_for_count_num(query, 26)

    def edit_count_100(self):
        """
        (27, '编辑主任', 2, '编辑主任', '编辑了100个帖子', 0, 0)
        """
        query = "SELECT count(*) vote_count, user_id FROM activity WHERE \
                    activity_type = %s OR \
                    activity_type = %s AND \
                    user_id NOT IN (SELECT user_id FROM award WHERE badge_id = %s) \
                    GROUP BY user_id HAVING vote_count >= 100" % (TYPE_ACTIVITY_UPDATE_QUESTION, TYPE_ACTIVITY_UPDATE_ANSWER, 27)

        self.__award_for_count_num(query, 27)

    def comment_count_10(self):
        """
        (5, '评论家', 3, '评论家', '评论10次以上', 0, 0),
        """
        query = "SELECT count(*) vote_count, user_id FROM activity WHERE \
                    activity_type = %s OR \
                    activity_type = %s AND \
                    user_id NOT IN (SELECT user_id FROM award WHERE badge_id = %s) \
                    GROUP BY user_id HAVING vote_count >= 10" % (TYPE_ACTIVITY_COMMENT_QUESTION, TYPE_ACTIVITY_COMMENT_ANSWER, 5)
        self.__award_for_count_num(query, 5)

    def __award_for_count_num(self, query, badge):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            awarded_users = []
            badge = get_object_or_404(Badge, id=badge)
            for row in rows:
                vote_count = row[0]
                user_id = row[1]

                if user_id not in awarded_users:
                    user = get_object_or_404(User, id=user_id)
                    award = Award(user=user, badge=badge)
                    award.save()
                    awarded_users.append(user_id)
        finally:
            cursor.close()

def main():
    pass

if __name__ == '__main__':
    main()
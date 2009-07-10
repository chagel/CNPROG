import datetime
import logging
from django.contrib.auth.models import User, UserManager
from django.db import connection, models, transaction
from django.db.models import Q
from forum.models import *

class QuestionManager(models.Manager):
    def update_tags(self, question, tagnames, user):
        """
        Updates Tag associations for a question to match the given
        tagname string.

        Returns ``True`` if tag usage counts were updated as a result,
        ``False`` otherwise.
        """
        from forum.models import Tag
        current_tags = list(question.tags.all())
        current_tagnames = set(t.name for t in current_tags)
        updated_tagnames = set(t for t in tagnames.split(' ') if t)
        modified_tags = []

        removed_tags = [t for t in current_tags
                        if t.name not in updated_tagnames]
        if removed_tags:
            modified_tags.extend(removed_tags)
            question.tags.remove(*removed_tags)

        added_tagnames = updated_tagnames - current_tagnames
        if added_tagnames:
            added_tags = Tag.objects.get_or_create_multiple(added_tagnames,
                                                            user)
            modified_tags.extend(added_tags)
            question.tags.add(*added_tags)

        if modified_tags:
            Tag.objects.update_use_counts(modified_tags)
            return True

        return False

    def update_answer_count(self, question):
        """
        Executes an UPDATE query to update denormalised data with the
        number of answers the given question has.
        """
        
        # for some reasons, this Answer class failed to be imported,
        # although we have imported all classes from models on top.
        from forum.models import Answer
        self.filter(id=question.id).update(
            answer_count=Answer.objects.get_answers_from_question(question).count())
    
    def update_view_count(self, question):
        """
        update counter+1 when user browse question page
        """
        self.filter(id=question.id).update(view_count = question.view_count + 1)
    
    def update_favorite_count(self, question):
        """
        update favourite_count for given question
        """
        from forum.models import FavoriteQuestion
        self.filter(id=question.id).update(favourite_count = FavoriteQuestion.objects.filter(question=question).count())
        
    def get_similar_questions(self, question):
        """
        Get 10 similar questions for given one.
        This will search the same tag list for give question(by exactly same string) first.
        Questions with the individual tags will be added to list if above questions are not full.
        """
        #print datetime.datetime.now()
        from forum.models import Question
        questions = list(Question.objects.filter(tagnames = question.tagnames).all())

        tags_list = question.tags.all()
        for tag in tags_list:
            extend_questions = Question.objects.filter(tags__id = tag.id)[:50]
            for item in extend_questions:
                if item not in questions and len(questions) < 10:
                    questions.append(item)
          
        #print datetime.datetime.now()
        return questions    
    
class TagManager(models.Manager):
    UPDATE_USED_COUNTS_QUERY = (
        'UPDATE tag '
        'SET used_count = ('
            'SELECT COUNT(*) FROM question_tags '
            'WHERE tag_id = tag.id'
        ') '
        'WHERE id IN (%s)')

    def get_or_create_multiple(self, names, user):
        """
        Fetches a list of Tags with the given names, creating any Tags
        which don't exist when necesssary.
        """
        tags = list(self.filter(name__in=names))
        #Set all these tag visible
        for tag in tags:
            if tag.deleted:
                tag.deleted = False
                tag.deleted_by = None
                tag.deleted_at = None
                tag.save()
                
        if len(tags) < len(names):
            existing_names = set(tag.name for tag in tags)
            new_names = [name for name in names if name not in existing_names]
            tags.extend([self.create(name=name, created_by=user)
                         for name in new_names if self.filter(name=name).count() == 0 and len(name.strip()) > 0])
             
        return tags

    def update_use_counts(self, tags):
        """Updates the given Tags with their current use counts."""
        if not tags:
            return
        cursor = connection.cursor()
        query = self.UPDATE_USED_COUNTS_QUERY % ','.join(['%s'] * len(tags))
        cursor.execute(query, [tag.id for tag in tags])
        transaction.commit_unless_managed()

class AnswerManager(models.Manager):
    GET_ANSWERS_FROM_USER_QUESTIONS = u'SELECT answer.* FROM answer INNER JOIN question ON answer.question_id = question.id WHERE question.author_id =%s AND answer.author_id <> %s'
    def get_answers_from_question(self, question, user=None):
        """
        Retrieves visibile answers for the given question. Delete answers
        are only visibile to the person who deleted them.
        """
       
        if user is None or not user.is_authenticated():
            return self.filter(question=question, deleted=False)
        else:
            return self.filter(Q(question=question),
                               Q(deleted=False) | Q(deleted_by=user))
                               
    def get_answers_from_questions(self, user_id):
        """
        Retrieves visibile answers for the given question. Which are not included own answers
        """
        cursor = connection.cursor()
        cursor.execute(self.GET_ANSWERS_FROM_USER_QUESTIONS, [user_id, user_id])
        return cursor.fetchall()

class VoteManager(models.Manager):
    COUNT_UP_VOTE_BY_USER = "SELECT count(*) FROM vote WHERE user_id = %s AND vote = 1"
    COUNT_DOWN_VOTE_BY_USER = "SELECT count(*) FROM vote WHERE user_id = %s AND vote = -1"
    COUNT_VOTES_PER_DAY_BY_USER = "SELECT COUNT(*) FROM vote WHERE user_id = %s AND DATE(voted_at) = DATE(NOW())"
    def get_up_vote_count_from_user(self, user):
        if user is not None:
            cursor = connection.cursor()
            cursor.execute(self.COUNT_UP_VOTE_BY_USER, [user.id])
            row = cursor.fetchone()
            return row[0]
        else:
            return 0
    
    def get_down_vote_count_from_user(self, user):
        if user is not None:
            cursor = connection.cursor()
            cursor.execute(self.COUNT_DOWN_VOTE_BY_USER, [user.id])
            row = cursor.fetchone()
            return row[0]
        else:
            return 0
            
    def get_votes_count_today_from_user(self, user):
        if user is not None:
            cursor = connection.cursor()
            cursor.execute(self.COUNT_VOTES_PER_DAY_BY_USER, [user.id])
            row = cursor.fetchone()
            return row[0]

        else:
            return 0
            
class FlaggedItemManager(models.Manager):
    COUNT_FLAGS_PER_DAY_BY_USER = "SELECT COUNT(*) FROM flagged_item WHERE user_id = %s AND DATE(flagged_at) = DATE(NOW())"
    def get_flagged_items_count_today(self, user):
        if user is not None:
            cursor = connection.cursor()
            cursor.execute(self.COUNT_FLAGS_PER_DAY_BY_USER, [user.id])
            row = cursor.fetchone()
            return row[0]

        else:
            return 0

class ReputeManager(models.Manager):
    COUNT_REPUTATION_PER_DAY_BY_USER = "SELECT SUM(positive)+SUM(negative) FROM repute WHERE user_id = %s AND (reputation_type=1 OR reputation_type=-8) AND DATE(reputed_at) = DATE(NOW())"
    def get_reputation_by_upvoted_today(self, user):
        """
        For one user in one day, he can only earn rep till certain score (ep. +200) 
        by upvoted(also substracted from upvoted canceled). This is because we need
        to prohibit gaming system by upvoting/cancel again and again.
        """
        if user is not None:
            cursor = connection.cursor()
            cursor.execute(self.COUNT_REPUTATION_PER_DAY_BY_USER, [user.id])
            row = cursor.fetchone()
            return row[0]

        else:
            return 0    
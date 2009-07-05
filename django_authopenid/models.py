# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

import hashlib, random, sys, os, time

__all__ = ['Nonce', 'Association', 'UserAssociation', 
        'UserPasswordQueueManager', 'UserPasswordQueue']

class Nonce(models.Model):
    """ openid nonce """
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)
    
    def __unicode__(self):
        return u"Nonce: %s" % self.id

    
class Association(models.Model):
    """ association openid url and lifetime """
    server_url = models.TextField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.TextField(max_length=255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length=64)
    
    def __unicode__(self):
        return u"Association: %s, %s" % (self.server_url, self.handle)

class UserAssociation(models.Model):
    """ 
    model to manage association between openid and user 
    """
    openid_url = models.CharField(blank=False, max_length=255)
    user = models.ForeignKey(User, unique=True)
    
    def __unicode__(self):
        return "Openid %s with user %s" % (self.openid_url, self.user)

class UserPasswordQueueManager(models.Manager):
    """ manager for UserPasswordQueue object """
    def get_new_confirm_key(self):
        "Returns key that isn't being used."
        # The random module is seeded when this Apache child is created.
        # Use SECRET_KEY as added salt.
        while 1:
            confirm_key = hashlib.md5("%s%s%s%s" % (
                random.randint(0, sys.maxint - 1), os.getpid(),
                time.time(), settings.SECRET_KEY)).hexdigest()
            try:
                self.get(confirm_key=confirm_key)
            except self.model.DoesNotExist:
                break
        return confirm_key


class UserPasswordQueue(models.Model):
    """
    model for new password queue.
    """
    user = models.ForeignKey(User, unique=True)
    new_password = models.CharField(max_length=30)
    confirm_key = models.CharField(max_length=40)

    objects = UserPasswordQueueManager()

    def __unicode__(self):
        return self.user.username

#!/usr/bin/env python
#encoding:utf-8
#-------------------------------------------------------------------------------
# Name:        Award badges command
# Purpose:     This is a command file croning in background process regularly to
#              query database and award badges for user's special acitivities.
#
# Author:      Mike, Sailing
#
# Created:     22/01/2009
# Copyright:   (c) Mike 2009
# Licence:     GPL V2
#-------------------------------------------------------------------------------

from datetime import datetime, date
from django.core.management.base import NoArgsCommand
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from forum.models import *
from forum.const import *

class BaseCommand(NoArgsCommand):
    def update_activities_auditted(self, cursor, activity_ids):
        # update processed rows to auditted
        if len(activity_ids):
            query = "UPDATE activity SET is_auditted = 1 WHERE id in (%s)"\
                    % ','.join('%s' % item for item in activity_ids)
            cursor.execute(query)
    
 
        
        
        

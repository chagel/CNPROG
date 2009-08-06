from django.core.management.base import NoArgsCommand
from django.db import connection
from forum.models import *
import collections
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _
import settings

class Command(NoArgsCommand):
    def handle_noargs(self,**options):
        try:
            self.send_email_alerts()
        except Exception, e:
            print e
        finally:
            connection.close()

    def send_email_alerts(self):
        report_time = datetime.datetime.now()
        feeds = EmailFeed.objects.all()
        user_ctype = ContentType.objects.get_for_model(User)

        #lists of update messages keyed by email address
        update_collection = collections.defaultdict(list) 
        for feed in feeds:
            update_summary = feed.get_update_summary()
            if update_summary != None:
                email = feed.get_email()
                update_collection[email].append(update_summary)
                feed.reported_at = report_time
                feed.save()

        for email, updates in update_collection.items():
            text = '\n'.join(updates)
            subject = _('updates from website')
            print 'sent %s to %s' % (updates,email)
            msg = EmailMessage(subject, text, settings.DEFAULT_FROM_EMAIL, [email])
            msg.content_subtype = 'html'
            msg.send()

            

from django.core.management.base import NoArgsCommand
from forum.models import Comment

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        objs = Comment.objects.all()
        print objs
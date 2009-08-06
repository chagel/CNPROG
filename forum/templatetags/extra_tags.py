import time
import datetime
import math
import re
import logging
from django import template
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
from forum.const import *
from django.utils.translation import ugettext as _

register = template.Library()

GRAVATAR_TEMPLATE = ('<img width="%(size)s" height="%(size)s" '
                     'src="http://www.gravatar.com/avatar/%(gravatar_hash)s'
                     '?s=%(size)s&d=identicon&r=PG">')

@register.simple_tag
def gravatar(user, size):
    """
    Creates an ``<img>`` for a user's Gravatar with a given size.

    This tag can accept a User object, or a dict containing the
    appropriate values.
    """
    try:
        gravatar = user['gravatar']
    except (TypeError, AttributeError, KeyError):
        gravatar = user.gravatar
    return mark_safe(GRAVATAR_TEMPLATE % {
        'size': size,
        'gravatar_hash': gravatar,
    })

MAX_FONTSIZE = 18
MIN_FONTSIZE = 12
@register.simple_tag
def tag_font_size(max_size, min_size, current_size):
    """
    do a logarithmic mapping calcuation for a proper size for tagging cloud
    Algorithm from http://blogs.dekoh.com/dev/2007/10/29/choosing-a-good-font-size-variation-algorithm-for-your-tag-cloud/
    """
    #avoid invalid calculation
    if current_size == 0:
        current_size = 1
    try:
        weight = (math.log10(current_size) - math.log10(min_size)) / (math.log10(max_size) - math.log10(min_size))
    except:
        weight = 0
    return MIN_FONTSIZE + round((MAX_FONTSIZE - MIN_FONTSIZE) * weight)


LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 5
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 4
NUM_PAGES_OUTSIDE_RANGE = 1
ADJACENT_PAGES = 2
@register.inclusion_tag("paginator.html")
def cnprog_paginator(context):
    """
    custom paginator tag
    Inspired from http://blog.localkinegrinds.com/2007/09/06/digg-style-pagination-in-django/
    """
    if (context["is_paginated"]):
        " Initialize variables "
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)

        if (context["pages"] <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = [n for n in range(1, context["pages"] + 1) if n > 0 and n <= context["pages"]]
        elif (context["page"] <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= context["pages"]]
            pages_outside_leading_range = [n + context["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (context["page"] > context["pages"] - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(context["pages"] - TRAILING_PAGE_RANGE_DISPLAYED + 1, context["pages"] + 1) if n > 0 and n <= context["pages"]]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else:
            page_numbers = [n for n in range(context["page"] - ADJACENT_PAGES, context["page"] + ADJACENT_PAGES + 1) if n > 0 and n <= context["pages"]]
            pages_outside_leading_range = [n + context["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

        extend_url = context.get('extend_url', '')
        return {
            "base_url": context["base_url"],
            "is_paginated": context["is_paginated"],
            "previous": context["previous"],
            "has_previous": context["has_previous"],
            "next": context["next"],
            "has_next": context["has_next"],
            "page": context["page"],
            "pages": context["pages"],
            "page_numbers": page_numbers,
            "in_leading_range" : in_leading_range,
            "in_trailing_range" : in_trailing_range,
            "pages_outside_leading_range": pages_outside_leading_range,
            "pages_outside_trailing_range": pages_outside_trailing_range,
            "extend_url" : extend_url
        }

@register.inclusion_tag("pagesize.html")
def cnprog_pagesize(context):
    """
    display the pagesize selection boxes for paginator
    """
    if (context["is_paginated"]):
        return {
            "base_url": context["base_url"],
            "pagesize" : context["pagesize"],
            "is_paginated": context["is_paginated"]
        }
        
@register.simple_tag
def get_score_badge(user):
    BADGE_TEMPLATE = '<span class="score" title="%(reputation)s %(reputationword)s">%(reputation)s</span>'
    if user.gold > 0 :
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(gold)s %(badgesword)s">'
        '<span class="badge1">&#9679;</span>'
        '<span class="badgecount">%(gold)s</span>'
        '</span>')
    if user.silver > 0:
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(silver)s %(badgesword)s">'
        '<span class="silver">&#9679;</span>'
        '<span class="badgecount">%(silver)s</span>'
        '</span>')
    if user.bronze > 0:
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(bronze)s %(badgesword)s">'
        '<span class="bronze">&#9679;</span>'
        '<span class="badgecount">%(bronze)s</span>'
        '</span>')
    BADGE_TEMPLATE = smart_unicode(BADGE_TEMPLATE, encoding='utf-8', strings_only=False, errors='strict')
    return mark_safe(BADGE_TEMPLATE % {
        'reputation' : user.reputation,
        'gold' : user.gold,
        'silver' : user.silver,
        'bronze' : user.bronze,
		'badgesword' : _('badges'),
		'reputationword' : _('reputation points'),
    })
    
@register.simple_tag
def get_score_badge_by_details(rep, gold, silver, bronze):
    BADGE_TEMPLATE = '<span class="reputation-score" title="%(reputation)s %(repword)s">%(reputation)s</span>'
    if gold > 0 :
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(gold)s %(badgeword)s">'
        '<span class="badge1">&#9679;</span>'
        '<span class="badgecount">%(gold)s</span>'
        '</span>')
    if silver > 0:
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(silver)s %(badgeword)s">'
        '<span class="badge2">&#9679;</span>'
        '<span class="badgecount">%(silver)s</span>'
        '</span>')
    if bronze > 0:
        BADGE_TEMPLATE = '%s%s' % (BADGE_TEMPLATE, '<span title="%(bronze)s %(badgeword)s">'
        '<span class="badge3">&#9679;</span>'
        '<span class="badgecount">%(bronze)s</span>'
        '</span>')
    BADGE_TEMPLATE = smart_unicode(BADGE_TEMPLATE, encoding='utf-8', strings_only=False, errors='strict')
    return mark_safe(BADGE_TEMPLATE % {
        'reputation' : rep,
        'gold' : gold,
        'silver' : silver,
        'bronze' : bronze,
		'repword' : _('reputation points'),
		'badgeword' : _('badges'),
    })      
    
@register.simple_tag
def get_user_vote_image(dic, key, arrow):
    if dic.has_key(key):
        if int(dic[key]) == int(arrow):
            return '-on'
    return ''
        
@register.simple_tag
def get_age(birthday):
    current_time = datetime.datetime(*time.localtime()[0:6])
    year = birthday.year
    month = birthday.month
    day = birthday.day
    diff = current_time - datetime.datetime(year,month,day,0,0,0)
    return diff.days / 365

@register.simple_tag
def get_total_count(up_count, down_count):
    return up_count + down_count

@register.simple_tag
def format_number(value):
    strValue = str(value)
    if len(strValue) <= 3:
        return strValue
    result = ''
    first = ''
    pattern = re.compile('(-?\d+)(\d{3})')
    m = re.match(pattern, strValue)
    while m != None:
        first = m.group(1)
        second = m.group(2)
        result = ',' + second + result
        strValue = first + ',' + second
        m = re.match(pattern, strValue)
    return first + result

@register.simple_tag
def convert2tagname_list(question):
    question['tagnames'] = [name for name in question['tagnames'].split(u' ')]
    return ''

@register.simple_tag
def diff_date(date, limen=2):
    current_time = datetime.datetime(*time.localtime()[0:6])
    diff = current_time - date
    diff_days = diff.days
    if diff_days > limen:
        return date
    else:
        return timesince(date) + _(' ago')
        
@register.simple_tag
def get_latest_changed_timestamp():
    try:
        from time import localtime, strftime
        from os import path
        from django.conf import settings
        root = settings.SITE_SRC_ROOT
        dir = (
            root,
            '%s/forum' % root,
            '%s/templates' % root,
        )
        stamp = (path.getmtime(d) for d in dir)
        latest = max(stamp)
        timestr = strftime("%H:%M %b-%d-%Y %Z", localtime(latest))
    except:
        timestr = ''
    return timestr

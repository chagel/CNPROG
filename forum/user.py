# coding=utf-8
from django.utils.translation import ugettext as _
class UserView:
    def __init__(self, id, tab_title, tab_description, page_title, view_name, template_file, data_size=0):
        self.id = id
        self.tab_title = tab_title
        self.tab_description = tab_description
        self.page_title = page_title
        self.view_name = view_name
        self.template_file = template_file
        self.data_size = data_size
        
        
USER_TEMPLATE_VIEWS = (
    UserView(
        id = 'stats',
        tab_title = _("Overview"),
        tab_description = _('User overview'),
        page_title = _('Overview - User Profile'),
        view_name = 'user_stats',
        template_file = 'user_stats.html'
    ),
    UserView(
        id = 'recent',
        tab_title = _('Recent'),
        tab_description = _("Recent activities"),
        page_title = _('Recent - User Profile'),
        view_name = 'user_recent',
        template_file = 'user_recent.html',
        data_size = 50
    ),
    UserView(
        id = 'responses',
        tab_title = _("Response"),
        tab_description = _("Responses from others"),
        page_title = _("Response - User Profile"),
        view_name = 'user_responses',
        template_file = 'user_responses.html',
        data_size = 50
    ),
    UserView(
        id = 'reputation',
        tab_title = _("Reputation"),
        tab_description = _("Community reputation"),
        page_title = _("Reputation - User Profile"),
        view_name = 'user_reputation',
        template_file = 'user_reputation.html'
    ),
    UserView(
        id = 'favorites',
        tab_title = _("Favorites"),
        tab_description = _("User's favorite questions"),
        page_title = _("Favorites - User Profile"),
        view_name = 'user_favorites',
        template_file = 'user_favorites.html',
        data_size = 50
    ),
    UserView(
        id = 'votes',
        tab_title = _("Votes"),
        tab_description = _("Votes history"),
        page_title = _("Votes - User Profile"),
        view_name = 'user_votes',
        template_file = 'user_votes.html',
        data_size = 50
    ),
    UserView(
        id = 'preferences',
        tab_title = _("Preferences"),
        tab_description = _("User preferences"),
        page_title = _("Preferences - User Profile"),
        view_name = 'user_preferences',
        template_file = 'user_preferences.html'
    )
)

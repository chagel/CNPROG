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
        tab_title = _('overview'),
        tab_description = _('user profile'),
        page_title = _('user profile overview'),
        view_name = 'user_stats',
        template_file = 'user_stats.html'
    ),
    UserView(
        id = 'recent',
        tab_title = _('recent activity'),
        tab_description = _('recent user activity'),
        page_title = _('profile - recent activity'),
        view_name = 'user_recent',
        template_file = 'user_recent.html',
        data_size = 50
    ),
    UserView(
        id = 'responses',
        tab_title = _('responses'),
        tab_description = _('comments and answers to others questions'),
        page_title = _('profile - responses'),
        view_name = 'user_responses',
        template_file = 'user_responses.html',
        data_size = 50
    ),
    UserView(
        id = 'reputation',
        tab_title = _('reputation'),
        tab_description = _('user reputation in the community'),
        page_title = _('profile - user reputation'),
        view_name = 'user_reputation',
        template_file = 'user_reputation.html'
    ),
    UserView(
        id = 'favorites',
        tab_title = _('favorite questions'),
        tab_description = _('users favorite questions'),
        page_title = _('profile - favorite questions'),
        view_name = 'user_favorites',
        template_file = 'user_favorites.html',
        data_size = 50
    ),
    UserView(
        id = 'votes',
        tab_title = _('casted votes'),
        tab_description = _('user vote record'),
        page_title = _('profile - votes'),
        view_name = 'user_votes',
        template_file = 'user_votes.html',
        data_size = 50
    ),
    UserView(
        id = 'preferences',
        tab_title = _('preferences'),
        tab_description = _('user preference settings'),
        page_title = _('profile - user preferences'),
        view_name = 'user_preferences',
        template_file = 'user_preferences.html'
    )
)

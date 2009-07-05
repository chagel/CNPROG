# coding=utf-8
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
        tab_title = u'概览',
        tab_description = u'用户概览',
        page_title = u'概览-用户资料',
        view_name = 'user_stats',
        template_file = 'user_stats.html'
    ),
    UserView(
        id = 'recent',
        tab_title = u'最近活动',
        tab_description = u'用户最近的活动状况',
        page_title = u'最近活动 - 用户资料',
        view_name = 'user_recent',
        template_file = 'user_recent.html',
        data_size = 50
    ),
    UserView(
        id = 'responses',
        tab_title = u'回应',
        tab_description = u'其他用户的回复和评论',
        page_title = u'回应 - 用户资料',
        view_name = 'user_responses',
        template_file = 'user_responses.html',
        data_size = 50
    ),
    UserView(
        id = 'reputation',
        tab_title = u'积分',
        tab_description = u'用户社区积分',
        page_title = u'积分 - 用户资料',
        view_name = 'user_reputation',
        template_file = 'user_reputation.html'
    ),
    UserView(
        id = 'favorites',
        tab_title = u'收藏',
        tab_description = u'用户收藏的问题',
        page_title = u'收藏 - 用户资料',
        view_name = 'user_favorites',
        template_file = 'user_favorites.html',
        data_size = 50
    ),
    UserView(
        id = 'votes',
        tab_title = u'投票',
        tab_description = u'用户所有投票',
        page_title = u'投票 - 用户资料',
        view_name = 'user_votes',
        template_file = 'user_votes.html',
        data_size = 50
    ),
    UserView(
        id = 'preferences',
        tab_title = u'设置',
        tab_description = u'用户参数设置',
        page_title = u'设置 - 用户资料',
        view_name = 'user_preferences',
        template_file = 'user_preferences.html'
    )
)
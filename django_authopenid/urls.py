# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('django_authopenid.views',
    # yadis rdf
    url(r'^yadis.xrdf$', 'xrdf', name='yadis_xrdf'),
     # manage account registration
    url(r'^%s$' % _('signin/'), 'signin', name='user_signin'),
    url(r'^%s$' % _('signout/'), 'signout', name='user_signout'),
    url(r'^%s%s$' % (_('signin/'), _('complete/')), 'complete_signin', 
        name='user_complete_signin'),
    url(r'^%s$' % _('register/'), 'register', name='user_register'),
    url(r'^%s$' % _('signup/'), 'signup', name='user_signup'),
    #disable current sendpw function
    url(r'^%s$' % _('sendpw/'), 'signin', name='user_sendpw'),
    #url(r'^%s$' % _('sendpw/'), 'sendpw', name='user_sendpw'),
    #url(r'^%s%s$' % (_('password/'), _('confirm/')), 'confirmchangepw', 
    #    name='user_confirmchangepw'),

    # manage account settings
    #url(r'^$', 'account_settings', name='user_account_settings'),
    #url(r'^%s$' % _('password/'), 'changepw', name='user_changepw'),
    #url(r'^%s$' % _('email/'), 'changeemail', name='user_changeemail'),
    #url(r'^%s$' % _('openid/'), 'changeopenid', name='user_changeopenid'),
    url(r'^%s$' % _('delete/'), 'delete', name='user_delete'),
)

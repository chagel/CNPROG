# -*- coding: utf-8 -*-
# Copyright (c) 2007, 2008, Benoît Chesneau
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#      * Redistributions of source code must retain the above copyright
#      * notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#      * notice, this list of conditions and the following disclaimer in the
#      * documentation and/or other materials provided with the
#      * distribution.  Neither the name of the <ORGANIZATION> nor the names
#      * of its contributors may be used to endorse or promote products
#      * derived from this software without specific prior written
#      * permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.conf import settings

import re


# needed for some linux distributions like debian
try:
    from openid.yadis import xri
except ImportError:
    from yadis import xri
    
from django_authopenid.util import clean_next

__all__ = ['OpenidSigninForm', 'OpenidAuthForm', 'OpenidVerifyForm',
        'OpenidRegisterForm', 'RegistrationForm', 'ChangepwForm',
        'ChangeemailForm', 'EmailPasswordForm', 'DeleteForm',
        'ChangeOpenidForm', 'ChangeEmailForm', 'ChangepwForm']

class OpenidSigninForm(forms.Form):
    """ signin form """
    openid_url = forms.CharField(max_length=255, widget=forms.widgets.TextInput(attrs={'class': 'openid-login-input', 'size':80}))
    next = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)

    def clean_openid_url(self):
        """ test if openid is accepted """
        if 'openid_url' in self.cleaned_data:
            openid_url = self.cleaned_data['openid_url']
            if xri.identifierScheme(openid_url) == 'XRI' and getattr(
                settings, 'OPENID_DISALLOW_INAMES', False
                ):
                raise forms.ValidationError(_('i-names are not supported'))
            return self.cleaned_data['openid_url']

    def clean_next(self):
        """ validate next """
        if 'next' in self.cleaned_data and self.cleaned_data['next'] != "":
            self.cleaned_data['next'] = clean_next(self.cleaned_data['next'])
            return self.cleaned_data['next']


attrs_dict = { 'class': 'required login' }
username_re = re.compile(r'^\w+$')
RESERVED_NAMES = (u'fuck', u'shit', u'ass', u'sex', u'add',
                   u'edit', u'save', u'delete', u'manage', u'update', 'remove', 'new')

class OpenidAuthForm(forms.Form):
    """ legacy account signin form """
    next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
            required=False)
    username = forms.CharField(max_length=30,  
            widget=forms.widgets.TextInput(attrs=attrs_dict))
    password = forms.CharField(max_length=128, 
            widget=forms.widgets.PasswordInput(attrs=attrs_dict))
       
    def __init__(self, data=None, files=None, auto_id='id_%s',
            prefix=None, initial=None): 
        super(OpenidAuthForm, self).__init__(data, files, auto_id,
                prefix, initial)
        self.user_cache = None
            
    def clean_username(self):
        """ validate username and test if it exists."""
        if 'username' in self.cleaned_data and \
                'openid_url' not in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(_("Usernames can only contain \
                    letters, numbers and underscores"))
            try:
                user = User.objects.get(
                        username__exact = self.cleaned_data['username']
                )
            except User.DoesNotExist:
                raise forms.ValidationError(_("This username does not exist \
                    in our database. Please choose another."))
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'There is already more than one \
                    account registered with that username. Please try \
                    another.')
            return self.cleaned_data['username']

    def clean_password(self):
        """" test if password is valid for this username """
        if 'username' in self.cleaned_data and \
                'password' in self.cleaned_data:
            self.user_cache =  authenticate(
                    username=self.cleaned_data['username'], 
                    password=self.cleaned_data['password']
            )
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a valid \
                    username and password. Note that both fields are \
                    case-sensitive."))
            elif self.user_cache.is_active == False:
                raise forms.ValidationError(_("This account is inactive."))
            return self.cleaned_data['password']

    def clean_next(self):
        """ validate next url """
        if 'next' in self.cleaned_data and \
                self.cleaned_data['next'] != "":
            self.cleaned_data['next'] = clean_next(self.cleaned_data['next'])
            return self.cleaned_data['next']
            
    def get_user(self):
        """ get authenticated user """
        return self.user_cache
            

class OpenidRegisterForm(forms.Form):
    """ openid signin form """
    next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
            required=False)
    username = forms.CharField(max_length=30, 
            widget=forms.widgets.TextInput(attrs=attrs_dict))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
        maxlength=200)), label=u'Email address')
    
    def clean_username(self):
        """ test if username is valid and exist in database """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(_('invalid user name'))
            if self.cleaned_data['username'] in RESERVED_NAMES:
                raise forms.ValidationError(_('sorry, this name can not be used, please try another'))
            if len(self.cleaned_data['username']) < settings.MIN_USERNAME_LENGTH:
                raise forms.ValidationError(_('username too short'))
            try:
                user = User.objects.get(
                        username__exact = self.cleaned_data['username']
                        )
            except User.DoesNotExist:
                return self.cleaned_data['username']
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(_('this name is already in use - please try anoter'))
            raise forms.ValidationError(_('this name is already in use - please try anoter'))
            
    def clean_email(self):
        """Optionally, for security reason one unique email in database"""
        if 'email' in self.cleaned_data:
            if settings.EMAIL_UNIQUE == True:
                    try:
                        user = User.objects.get(email = self.cleaned_data['email'])
                    except User.DoesNotExist:
                        return self.cleaned_data['email']
                    except User.MultipleObjectsReturned:
                        raise forms.ValidationError(u'There is already more than one \
                            account registered with that e-mail address. Please try \
                            another.')
                    raise forms.ValidationError(_("This email is already \
                        registered in our database. Please choose another."))
            else:
                return self.cleaned_data['email']
        #what if not???
    
class OpenidVerifyForm(forms.Form):
    """ openid verify form (associate an openid with an account) """
    next = forms.CharField(max_length=255, widget = forms.HiddenInput(), 
            required=False)
    username = forms.CharField(max_length=30, 
            widget=forms.widgets.TextInput(attrs=attrs_dict))
    password = forms.CharField(max_length=128, 
            widget=forms.widgets.PasswordInput(attrs=attrs_dict))
    
    def __init__(self, data=None, files=None, auto_id='id_%s',
            prefix=None, initial=None): 
        super(OpenidVerifyForm, self).__init__(data, files, auto_id,
                prefix, initial)
        self.user_cache = None

    def clean_username(self):
        """ validate username """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(_('invalid user name'))
            try:
                user = User.objects.get(
                        username__exact = self.cleaned_data['username']
                )
            except User.DoesNotExist:
                raise forms.ValidationError(_("This username don't exist. \
                        Please choose another."))
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'Somehow, that username is in \
                    use for multiple accounts. Please contact us to get this \
                    problem resolved.')
            return self.cleaned_data['username']
            
    def clean_password(self):
        """ test if password is valid for this user """
        if 'username' in self.cleaned_data and \
                'password' in self.cleaned_data:
            self.user_cache =  authenticate(
                    username = self.cleaned_data['username'], 
                    password = self.cleaned_data['password']
            )
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a valid \
                    username and password. Note that both fields are \
                    case-sensitive."))
            elif self.user_cache.is_active == False:
                raise forms.ValidationError(_("This account is inactive."))
            return self.cleaned_data['password']
            
    def get_user(self):
        """ get authenticated user """
        return self.user_cache


attrs_dict = { 'class': 'required' }
username_re = re.compile(r'^[\w ]+$')

class RegistrationForm(forms.Form):
    """ legacy registration form """

    next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
            required=False)
    username = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs=attrs_dict),
            label=_('choose a username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
            maxlength=200)), label=_('your email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
            label=_('choose password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
            label=_('retype password'))

    def clean_username(self):
        """
        Validates that the username is alphanumeric and is not already
        in use.
        
        """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(u'Usernames can only contain \
                        letters, numbers and underscores')
            try:
                user = User.objects.get(
                        username__exact = self.cleaned_data['username']
                )

            except User.DoesNotExist:
                return self.cleaned_data['username']
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'Somehow, that username is in \
                    use for multiple accounts. Please contact us to get this \
                    problem resolved.')
            raise forms.ValidationError(u'This username is already taken. \
                    Please choose another.')

    def clean_email(self):
        """ validate if email exist in database
        :return: raise error if it exist """
        if 'email' in self.cleaned_data:
            if settings.EMAIL_UNIQUE == True:
                try:
                    user = User.objects.get(email = self.cleaned_data['email'])
                except User.DoesNotExist:
                    return self.cleaned_data['email']
                except User.MultipleObjectsReturned:
                    raise forms.ValidationError(u'There is already more than one \
                        account registered with that e-mail address. Please try \
                        another.')
                raise forms.ValidationError(u'This email is already registered \
                        in our database. Please choose another.')
            else:
                return self.cleaned_data['email']
        #what if not?
    
    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if 'password1' in self.cleaned_data and \
                'password2' in self.cleaned_data and \
                self.cleaned_data['password1'] == \
                self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(u'You must type the same password each \
                time')


class ChangepwForm(forms.Form):
    """ change password form """
    oldpw = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))

    def __init__(self, data=None, user=None, *args, **kwargs):
        if user is None:
            raise TypeError("Keyword argument 'user' must be supplied")
        super(ChangepwForm, self).__init__(data, *args, **kwargs)
        self.user = user

    def clean_oldpw(self):
        """ test old password """
        if not self.user.check_password(self.cleaned_data['oldpw']):
            raise forms.ValidationError(_("Old password is incorrect. \
                    Please enter the correct password."))
        return self.cleaned_data['oldpw']
    
    def clean_password2(self):
        """
        Validates that the two password inputs match.
        """
        if 'password1' in self.cleaned_data and \
                'password2' in self.cleaned_data and \
           self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(_("new passwords do not match"))
        
        
class ChangeemailForm(forms.Form):
    """ change email form """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
        maxlength=200)), label=u'Email address')
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, \
            initial=None, user=None):
        if user is None:
            raise TypeError("Keyword argument 'user' must be supplied")
        super(ChangeemailForm, self).__init__(data, files, auto_id, 
                prefix, initial)
        self.test_openid = False
        self.user = user
        
        
    def clean_email(self):
        """ check if email don't exist """
        if 'email' in self.cleaned_data:
            if settings.EMAIL_UNIQUE == True:
                if self.user.email != self.cleaned_data['email']:
                    try:
                        user = User.objects.get(email = self.cleaned_data['email'])
                    except User.DoesNotExist:
                        return self.cleaned_data['email']
                    except User.MultipleObjectsReturned:
                        raise forms.ValidationError(u'There is already more than one \
                            account registered with that e-mail address. Please try \
                            another.')
                    raise forms.ValidationError(u'This email is already registered \
                        in our database. Please choose another.')
            else:
                return self.cleaned_data['email']
        #what if not?
        

    def clean_password(self):
        """ check if we have to test a legacy account or not """
        if 'password' in self.cleaned_data:
            if not self.user.check_password(self.cleaned_data['password']):
                self.test_openid = True
        return self.cleaned_data['password']
                
class ChangeopenidForm(forms.Form):
    """ change openid form """
    openid_url = forms.CharField(max_length=255,
            widget=forms.TextInput(attrs={'class': "required" }))

    def __init__(self, data=None, user=None, *args, **kwargs):
        if user is None:
            raise TypeError("Keyword argument 'user' must be supplied")
        super(ChangeopenidForm, self).__init__(data, *args, **kwargs)
        self.user = user

class DeleteForm(forms.Form):
    """ confirm form to delete an account """
    confirm = forms.CharField(widget=forms.CheckboxInput(attrs=attrs_dict))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))

    def __init__(self, data=None, files=None, auto_id='id_%s',
            prefix=None, initial=None, user=None):
        super(DeleteForm, self).__init__(data, files, auto_id, prefix, initial)
        self.test_openid = False
        self.user = user

    def clean_password(self):
        """ check if we have to test a legacy account or not """
        if 'password' in self.cleaned_data:
            if not self.user.check_password(self.cleaned_data['password']):
                self.test_openid = True
        return self.cleaned_data['password']


class EmailPasswordForm(forms.Form):
    """ send new password form """
    username = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs={'class': "required" }))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
            initial=None):
        super(EmailPasswordForm, self).__init__(data, files, auto_id, 
                prefix, initial)
        self.user_cache = None


    def clean_username(self):
        """ get user for this username """
        if 'username' in self.cleaned_data:
            try:
                self.user_cache = User.objects.get(
                        username = self.cleaned_data['username'])
            except:
                raise forms.ValidationError(_("Incorrect username."))
        return self.cleaned_data['username']

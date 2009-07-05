import re
from datetime import date
from django import forms
from models import *
from const import *

class TitleField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 70, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = u'标题'
        self.help_text = u'请输入对问题具有描述性质的标题 - “帮忙！紧急求助！”不是建议的提问方式。'
        self.initial = ''

    def clean(self, value):
        if len(value) < 10:
            raise forms.ValidationError(u"标题的长度必须大于10")

        return value

class EditorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(EditorField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.Textarea(attrs={'id':'editor'})
        self.label  = u'内容'
        self.help_text = u''
        self.initial = ''

    def clean(self, value):
        if len(value) < 10:
            raise forms.ValidationError(u"内容至少要10个字符")

        return value

class TagNamesField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TagNamesField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 255
        self.label  = u'标签'
        self.help_text = u'多个标签请用空格间隔-最多5个标签。（优先使用自动匹配的英文标签。）'
        self.initial = ''

    def clean(self, value):
        value = super(TagNamesField, self).clean(value)
        data = value.strip()
        if len(data) < 1:
            raise forms.ValidationError(u'标签不能为空')
        list = data.split(' ')
        list_temp = []
        if len(list) > 5:
            raise forms.ValidationError(u'最多只能有5个标签')
        for tag in list:
            if len(tag) > 20:
                raise forms.ValidationError(u'每个标签的长度不超过20')

            #TODO: regex match not allowed characters here

            if tag.find('/') > -1 or tag.find('\\') > -1 or tag.find('<') > -1 or tag.find('>') > -1 or tag.find('&') > -1 or tag.find('\'') > -1 or tag.find('"') > -1:
            #if not tagname_re.match(tag):
                raise forms.ValidationError(u'标签请使用英文字母，中文或者数字字符串（. - _ # 也可以）')
            # only keep one same tag
            if tag not in list_temp and len(tag.strip()) > 0:
                list_temp.append(tag)
        return u' '.join(list_temp)

class WikiField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super(WikiField, self).__init__(*args, **kwargs)
        self.required = False
        self.label  = u'社区wiki模式'
        self.help_text = u'选择社区wiki模式，问答不计算积分，签名也不显示作者信息'


class SummaryField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(SummaryField, self).__init__(*args, **kwargs)
        self.required = False
        self.widget = forms.TextInput(attrs={'size' : 50, 'autocomplete' : 'off'})
        self.max_length = 300
        self.label  = u'更新概要：'
        self.help_text = u'输入本次修改的简单概述（如：修改了别字，修正了语法，改进了样式等。非必填项。）'

class AskForm(forms.Form):
    title  = TitleField()
    text   = EditorField()
    tags   = TagNamesField()
    wiki = WikiField()

    openid = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 40, 'class':'openid-input'}))
    user   = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    email  = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))



class AnswerForm(forms.Form):
    text   = EditorField()
    wiki   = WikiField()
    openid = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 40, 'class':'openid-input'}))
    user   = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    email  = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if question.wiki:
            self.fields['wiki'].initial = True

class CloseForm(forms.Form):
    reason = forms.ChoiceField(choices=CLOSE_REASONS)

class RetagQuestionForm(forms.Form):
    tags   = TagNamesField()
    # initialize the default values
    def __init__(self, question, *args, **kwargs):
        super(RetagQuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].initial = question.tagnames

class RevisionForm(forms.Form):
    """
    Lists revisions of a Question or Answer
    """
    revision = forms.ChoiceField(widget=forms.Select(attrs={'style' : 'width:520px'}))

    def __init__(self, post, latest_revision, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)
        revisions = post.revisions.all().values_list(
            'revision', 'author__username', 'revised_at', 'summary')
        date_format = '%c'
        self.fields['revision'].choices = [
            (r[0], u'%s - %s (%s) %s' % (r[0], r[1], r[2].strftime(date_format), r[3]))
            for r in revisions]
        self.fields['revision'].initial = latest_revision.revision

class EditQuestionForm(forms.Form):
    title  = TitleField()
    text   = EditorField()
    tags   = TagNamesField()
    summary = SummaryField()

    def __init__(self, question, revision, *args, **kwargs):
        super(EditQuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].initial = revision.title
        self.fields['text'].initial = revision.text
        self.fields['tags'].initial = revision.tagnames
        # Once wiki mode is enabled, it can't be disabled
        if not question.wiki:
            self.fields['wiki'] = WikiField()

class EditAnswerForm(forms.Form):
    text = EditorField()
    summary = SummaryField()

    def __init__(self, answer, revision, *args, **kwargs):
        super(EditAnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].initial = revision.text

class EditUserForm(forms.Form):
    email = forms.EmailField(label=u'Email', help_text=u'不会公开，用于头像显示服务', required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    realname = forms.CharField(label=u'真实姓名', required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    website = forms.URLField(label=u'个人网站', required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    city = forms.CharField(label=u'城市', required=False, max_length=255, widget=forms.TextInput(attrs={'size' : 35}))
    birthday = forms.DateField(label=u'生日', help_text=u'不会公开，只会显示您的年龄，格式为：YYYY-MM-DD', required=True, widget=forms.TextInput(attrs={'size' : 35}))
    about = forms.CharField(label=u'个人简介', required=False, widget=forms.Textarea(attrs={'cols' : 60}))

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = user.email
        self.fields['realname'].initial = user.real_name
        self.fields['website'].initial = user.website
        self.fields['city'].initial = user.location

        if user.date_of_birth is not None:
            self.fields['birthday'].initial = user.date_of_birth.date()
        else:
            self.fields['birthday'].initial = '1990-01-01'
        self.fields['about'].initial = user.about
        self.user = user

    def clean_email(self):
        """For security reason one unique email in database"""
        if self.user.email != self.cleaned_data['email']:
            if 'email' in self.cleaned_data:
                try:
                    user = User.objects.get(email = self.cleaned_data['email'])
                except User.DoesNotExist:
                    return self.cleaned_data['email']
                except User.MultipleObjectsReturned:
                    raise forms.ValidationError(u'该电子邮件已被注册，请选择另一个再试。')
                raise forms.ValidationError("该电子邮件帐号已被注册，请选择另一个再试。")
        else:
            return self.cleaned_data['email']
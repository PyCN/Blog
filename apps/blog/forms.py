# coding:utf-8
from django import forms
from .models import Article, BlogComment


SEX_CHOICES = (
    ('male', '男'),
    ('female', '女')

)


class RegistForm(forms.Form):
    email = forms.EmailField(
        required=True, label='邮箱', error_messages={'required': '请输入邮箱'})
    username = forms.CharField(
        required=True, label='昵称 ', error_messages={'required': '请输入昵称'})
    password1 = forms.CharField(required=True, label='密码   ', widget=forms.PasswordInput(),
                                error_messages={'required': '请输入密码'})
    password2 = forms.CharField(required=True, label='确认密码', widget=forms.PasswordInput(),
                                error_messages={'required': '请再次输入密码'})
    sex = forms.ChoiceField(widget=forms.RadioSelect,
                            choices=SEX_CHOICES, label="性别")
    phone = forms.CharField(required=True, label='手机',
                            error_messages={'required': '请输入手机'})
    userimg = forms.ImageField(required=False, label='头像')


class UserForm(forms.Form):
    username = forms.EmailField(
        required=True, label='邮箱', error_messages={'required': '请输入邮箱'})
    password = forms.CharField(required=True, label='密码  ', widget=forms.PasswordInput(),
                               error_messages={'required': '请输入密码'})

    # def clean(self):
    #    if not self.is_valid():
    #        raise forms.ValidationError('用户名和密码为必填项')
    #    else:
    #        cleaned_data = super(UserForm, self).clean()


class RetrieveForm(forms.Form):
    username = forms.EmailField(
        required=True, label='邮箱', error_messages={'required': '请输入邮箱'})
    phone = forms.CharField(required=True, label='手机',
                            error_messages={'required': '请输入手机号'})
    password1 = forms.CharField(required=True, label='密码   ', widget=forms.PasswordInput(),
                                error_messages={'required': '请输入新密码'})
    password2 = forms.CharField(required=True, label='确认密码', widget=forms.PasswordInput(),
                                error_messages={'required': '请再次输入新密码'})


class SearchForm(forms.Form):
    body_search = forms.CharField(required=True)


class AttachmentForm(forms.Form):
    attachment = forms.FileInput()


class BlogCommentForm(forms.Form):
    body = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': '我来评两句~'}))

    '''class Meta:
        model = BlogComment
        
        fields = ['body']
        fields.is_required = True
        widgets = {'body': forms.Textarea(attrs={'placeholder': '我来评两句~'})}
        
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入昵称",
                'aria-describedby': "sizing-addon1",
            }),
            'user_email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入邮箱",
                'aria-describedby': "sizing-addon1",
            }),
            'body': forms.Textarea(attrs={'placeholder': '我来评两句~'}),
        }
        '''

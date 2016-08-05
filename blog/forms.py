#coding:utf-8
from django import forms
from .models import Article, BlogComment


class UserForm(forms.Form): 
    username = forms.EmailField(label='用户名')
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['user_name', 'user_email', 'body']
        widgets = {
            # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">
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

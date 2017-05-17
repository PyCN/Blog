from django import forms
from blog.models import *


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'


class SettingForm(forms.Form):
    title = forms.CharField(max_length=80, required=True)
    keywords = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=200, required=True)
    nickname = forms.CharField(max_length=100, required=True)
    homedescription = forms.CharField(max_length=150, required=True)
    recordinfo = forms.CharField(max_length=100, required=True)
    statisticalcode = forms.Textarea()

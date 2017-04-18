__author__ = 'forestg'
from django import forms

from django.db import models

from .models import MyPost
from .models import MyParse
from .models import MyMultiParse

class PostForm(forms.ModelForm):
    class Meta:
        model = MyPost
        fields = ('title', 'body', 'category', 'labels',)

class PostParse(forms.ModelForm):
    class Meta:
        model = MyParse
        field = ('linkString')

class MultiplePostParse(forms.ModelForm):
    class Meta:
        model = MyMultiParse
        field = ('linkText')

class webArticle(forms.ModelForm):
    class article(models.Model):
        textBody = models.TextField()
        category = models.CharField(max_length = 100)



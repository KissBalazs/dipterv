# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils import timezone

# Create your models here.
class MyPost(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    body = models.TextField()
    labels = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    category = models.CharField(max_length=150)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __unicode__(self): # %%! csak így működik magyar karakterekkel!!!
        return self.title

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')

class MyParse(models.Model):
    linkString = models.CharField(max_length=200)

class MyMultiParse(models.Model):
    linkTexts = models.TextField()

admin.site.register(MyPost, PostAdmin)


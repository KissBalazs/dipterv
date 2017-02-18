# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import MyPost
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from .forms import PostForm
from .forms import PostParse
from .forms import MultiplePostParse
from editor.topicmodeller.topicmodellerServices import yieldLabels # sajat api
from editor.topicmodeller.webParser import getWebContent # sasjat api 2
from editor.topicmodeller.webParser import getPostLabels
from editor.topicmodeller.webParser import getLinks
from editor.topicmodeller.webParser import parse_title

def post_list(request):
    posts = MyPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(MyPost, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.labels = yieldLabels(request.POST["body"], request.POST["labels"])
            post.save()
            return redirect('editor.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

def url_parse(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.labels = yieldLabels(request.POST["body"], request.POST["labels"])
            post.save()
            return redirect('editor.views.post_detail', pk=post.pk)

        parsedText = getWebContent(request.POST["linkString"])

        form = PostForm(initial={'body': parsedText})

        return render(request, 'post_edit.html', {'form': form})
    else:
        form = PostParse()
    return render(request, 'url_parse_edit.html' , {'form': form})


# todo: not real!
def add_to_corpus(request):
    if request.method == "POST":
        szoveg = request.POST("textArea")
        category = indexTopicModeller.addToCorpus(szoveg)
        return render(request, 'parse_menu_index.html', {'categoryResult':category})

def url_multi_parse(request):
    if request.method == "POST":

        links = getLinks(request.POST["linkTexts"])

        deleteMeTemp = 0;
        for link in links:
                deleteMeTemp += 1
                form = PostForm()
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.body = getWebContent(link)
                post.title = 'Parsed: ' + parse_title(link)
                originalTags = u' '.join(getPostLabels(link))
                #originalTags = "Teszteleshez eltavolitva " + str(deleteMeTemp)
                post.labels = yieldLabels(post.body, originalTags)
                post.category = u'Parsed'
                post.save()
        return HttpResponseRedirect("/")


    else:
        form = MultiplePostParse()
    return render(request, 'url_multi_parse_edit.html', {'form':form})


















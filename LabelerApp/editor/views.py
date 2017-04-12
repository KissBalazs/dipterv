# -*- coding: utf-8 -*-
# from django.shortcuts import render
import json
import os

import datetime

import operator
from django.shortcuts import redirect
from django.utils import timezone
from gensim import corpora

from editor.topicmodeller.services.indexHuTopicModelling import create_dictionary_index
from editor.topicmodeller.utils.consts import IndexDocumentsPath, IndexDictionaryPath, IndexFrequenciesPath
from editor.webcrawler.webcrawler.scripts.index_frontpage_parse import parse_index_hu
from editor.webcrawler.webcrawler.scripts.wiki_frontpage_parse import parse_wiki_hu
from .models import MyPost
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from .forms import PostForm
from .forms import PostParse
from .forms import MultiplePostParse
from editor.topicmodeller.topicmodellerServices import yieldLabels  # sajat api
from editor.topicmodeller.webParser import getWebContent  # sasjat api 2
from editor.topicmodeller.webParser import getPostLabels
from editor.topicmodeller.webParser import getLinks
from editor.topicmodeller.webParser import parse_title
from django.contrib.auth.decorators import login_required


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
    return render(request, 'url_parse_edit.html', {'form': form})


# # todo: not real!
# @login_required
# def add_to_corpus(request):
#     if request.method == "POST":
#         szoveg = request.POST("textArea")
#         category = indexTopicModeller.addToCorpus(szoveg)
#         return render(request, 'parse_menu_index.html', {'categoryResult':category})

@login_required
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
            # originalTags = "Teszteleshez eltavolitva " + str(deleteMeTemp)
            post.labels = yieldLabels(post.body, originalTags)
            post.category = u'Parsed'
            post.save()
        return HttpResponseRedirect("/")


    else:
        form = MultiplePostParse()
    return render(request, 'url_multi_parse_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(MyPost, pk=pk)
    post.delete()
    return redirect('post_list')


def parse_index(request):
    parse_index_hu()

    return HttpResponseRedirect('/')


def static_parse_page(request):
    wiki_path = "/home/forestg/projects/dipterv/LabelerApp/data/wiki.json"
    index_path = "/home/forestg/projects/dipterv/LabelerApp/data/index.json"
    if (os.path.isfile(wiki_path)):
        create_date_wiki = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(wiki_path))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_wiki = "nem létezik a fájl"

    if (os.path.isfile(index_path)):
        create_date_index = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(index_path))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_index = "nem létezik a fájl"

    if (os.path.isfile(IndexFrequenciesPath)):
        create_date_index_freq = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(IndexFrequenciesPath))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_index_freq = "nem létezik a fájl"


    return render(request, 'webparser/static_parse_page.html', {'create_date_wiki': create_date_wiki, 'create_date_index':create_date_index, 'create_date_index_freq':create_date_index_freq})


def static_parse_page_wiki_documents(request):
    path = "/home/forestg/projects/dipterv/LabelerApp/data/wiki.json"
    if (os.path.isfile(path)):
        with open(path) as data_file:
            document_array = json.load(data_file)
    else:
        document_array = [{
        "id":"0",
        "lang":"",
        "url":"Nem létezik a dokumentumtér.",
        "title":"",
        "text":""
        }]

    return render(request, 'webparser/static_parse_page_wiki_documents.html',{'document_array':document_array})

def static_parse_page_wiki_refresh_documents(request):
    parse_wiki_hu()
    return redirect('static_parse_page_wiki_documents')


def static_parse_page_index_documents(request):
    path = IndexDocumentsPath
    if (os.path.isfile(path)):
        with open(path) as data_file:
            document_array = json.load(data_file)
    else:
        document_array = [{
        "id":"0",
        "url":"Nem létezik a dokumentumtér.",
        "title":"",
        "text":""
        }]

    return render(request, 'webparser/static_parse_page_index_documents.html',{'document_array':document_array})

def static_parse_page_index_refresh_documents(request):
    parse_index_hu()
    return redirect('static_parse_page_index_documents')

def static_parse_page_index_refresh_dictionary(request):
    create_dictionary_index()
    return redirect('static_parse_page')

def static_parse_page_index_show_dictionary(request):
    path = IndexFrequenciesPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            frequencies = json.load(data_file)
        sortedDictionary =  sorted(frequencies.items(), key=operator.itemgetter(1))
    else:
        sortedDictionary = {["nem létezik még az fájl",""]}

    return render(request, 'webparser/static_parse_page_index_dictionary.html',{'sortedDictionary':sortedDictionary, 'size':len(sortedDictionary)})

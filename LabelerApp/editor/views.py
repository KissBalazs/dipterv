# -*- coding: utf-8 -*-
# from django.shortcuts import render
import json
import os

import datetime

import operator
from django.shortcuts import redirect
from django.utils import timezone
from gensim import corpora

from editor.topicmodeller.services.dynamicServices import linkListHandling, parseWebsitesFromLinkList, topicModelDynamic
from editor.topicmodeller.services.indexHuTopicModelling import create_dictionary_index, topic_model_index_hu
from editor.topicmodeller.services.wikiHuTopicModelling import create_dictionary_wiki, topic_model_wiki_hu
from editor.topicmodeller.utils.consts import IndexDocumentsPath, IndexDictionaryPath, IndexFrequenciesPath, \
    WikiFrequenciesPath, IndexTopicsPath2, WikiTopicsPath2, linkListPath, linkListDocumentsPath, DynamicTopicsPath
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
    if (os.path.isfile(WikiFrequenciesPath)):
        create_date_wiki_freq = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(WikiFrequenciesPath))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_wiki_freq = "nem létezik a fájl"
    if (os.path.isfile(IndexTopicsPath2)):
        create_date_index_topics = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(IndexTopicsPath2))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_index_topics = "nem létezik a fájl"
    if (os.path.isfile(WikiTopicsPath2)):
        create_date_wiki_topics = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(WikiTopicsPath2))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_wiki_topics = "nem létezik a fájl"

    return render(request, 'webparser/static_parse_page.html', {'create_date_wiki': create_date_wiki, 'create_date_index':create_date_index,
                                                                'create_date_index_freq':create_date_index_freq, 'create_date_wiki_freq':create_date_wiki_freq,
                                                                'create_date_index_topics':create_date_index_topics, 'create_date_wiki_topics':create_date_wiki_topics})


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



# WIKI parszolások
def static_parse_page_wiki_refresh_documents(request):
    parse_wiki_hu()
    return redirect('static_parse_page_wiki_documents')

def static_parse_page_wiki_show_dictionary(request):
    path = WikiFrequenciesPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            frequencies = json.load(data_file)
        sortedDictionary =  sorted(frequencies.items(), key=operator.itemgetter(1))
    else:
        sortedDictionary = {["nem létezik még az fájl",""]}

    return render(request, 'webparser/static_parse_page_wiki_dictionary.html',{'sortedDictionary':sortedDictionary, 'size':len(sortedDictionary)})

def static_parse_page_wiki_refresh_dictionary(request):
    create_dictionary_wiki()
    return redirect('static_parse_page')

def static_parse_page_wiki_topicmodel_start(request):
    topic_model_wiki_hu()
    return redirect('static_parse_page')

def static_parse_page_wiki_show_topicmodel(request):
    path = WikiTopicsPath2
    if (os.path.exists(path)):
        with open(path) as data_file:
            wikiTopicsJson = json.load(data_file)
        wikiTopics =  sorted(wikiTopicsJson.items(), key=operator.itemgetter(0))
    else:
        wikiTopics = {["nem létezik még az fájl",""]}
    return render(request, 'webparser/static_parse_page_wiki_topics.html',{'wikiTopics':wikiTopics})











# INDEX parszolások
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

def static_parse_page_index_topicmodel_start(request):
    topic_model_index_hu()
    return redirect('static_parse_page')


def static_parse_page_index_show_topicmodel(request):
    path = IndexTopicsPath2
    if (os.path.exists(path)):
        with open(path) as data_file:
            indexTopicsJson = json.load(data_file)
        indexTopics =  sorted(indexTopicsJson.items(), key=operator.itemgetter(0))
    else:
        indexTopics = {["nem létezik még az fájl",""]}
    print(indexTopics)
    return render(request, 'webparser/static_parse_page_index_topics.html',{'indexTopics':indexTopics})








# DINAMIKUS

def dynamic_parse_page(request):
    if (os.path.isfile(linkListPath)):
        with open(linkListPath) as data_file:
            linksCount = len(json.load(data_file))
    else:
        linksCount = 0
    if (os.path.isfile(linkListDocumentsPath)):
        create_date_dynamic_doc = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(linkListDocumentsPath))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_dynamic_doc = "nem létezik a fájl"

    if (os.path.isfile(DynamicTopicsPath)):
        create_date_dynamic_topics = datetime.datetime.fromtimestamp(
            int(os.path.getmtime(DynamicTopicsPath))
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        create_date_dynamic_topics = "nem létezik a fájl"
    return render(request, 'webparser/dynamic_parse_page.html', {'linksCount':linksCount, 'create_date_dynamic_doc':create_date_dynamic_doc, 'create_date_dynamic_topics': create_date_dynamic_topics})

def dynamic_parse_page_links_new(request):
    if request.method == "POST":
        linkListHandling(request.POST["linkTexts"])
        return redirect('dynamic_parse_page_links_list')
    else:
        form = MultiplePostParse()
    return render(request, 'webparser/dynamic_parse_page_links_new.html', {'form': form})

def dynamic_parse_page_links_list(request):
    path = linkListPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            links = json.load(data_file)
    else:
        links = {["nem létezik még az fájl"]}
    return render(request, 'webparser/dynamic_parse_page_links_list.html', {'links':links})

def dynamic_parse_page_document_parse(request):
    parseWebsitesFromLinkList()
    return redirect('dynamic_parse_page_document_list')

def dynamic_parse_page_document_list(request):
    path = linkListDocumentsPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            document_array = json.load(data_file)
    else:
        document_array = {"nem létezik még az fájl"}
    return render(request, 'webparser/dynamic_parse_page_document_list.html', {'document_array':document_array})


def dynamic_parse_page_topicmodel_create(request):
    topicModelDynamic()
    return redirect('dynamic_parse_page_topicmodel_list')

def dynamic_parse_page_topicmodel_list(request):
    path = DynamicTopicsPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            topic_array = json.load(data_file)
    else:
         topic_array = {"nem létezik még az fájl"}
    return render(request, 'webparser/dynamic_parse_page_topicmodel_list.html',{'topic_array':topic_array})


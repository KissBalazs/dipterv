__author__ = 'forestg'
from django.conf.urls import patterns, url, include
# from editor.views import newpost
# from editor.views import get_name
from editor.views import post_new, parse_index
from editor.views import post_list
from editor.views import post_detail
from editor.views import url_parse
from editor.views import url_multi_parse
from . import views

urlpatterns = patterns('',

    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', post_detail),
    url(r'^post/new/$', post_new, name='post_new'),
    url(r'^post/parse/$', url_parse, name='url_parse'),
    url(r'^post/parse_index/$', parse_index, name='parse_index'),
    url(r'^post/multiParse/$', url_multi_parse, name='url_multi_parse'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),



    url(r'^static_parse_page$', views.static_parse_page, name='static_parse_page'),

    url(r'^static_parse_page/static_parse_page_wiki_documents', views.static_parse_page_wiki_documents, name='static_parse_page_wiki_documents'),
    url(r'^static_parse_page/static_parse_page_wiki_refresh_documents', views.static_parse_page_wiki_refresh_documents, name='static_parse_page_wiki_refresh_documents'),
    url(r'^static_parse_page/static_parse_page_wiki_refresh_dictionary', views.static_parse_page_wiki_refresh_dictionary, name='static_parse_page_wiki_refresh_dictionary'),
    url(r'^static_parse_page/static_parse_page_wiki_show_dictionary', views.static_parse_page_wiki_show_dictionary, name='static_parse_page_wiki_show_dictionary'),
    url(r'^static_parse_page/static_parse_page_wiki_topicmodel_start', views.static_parse_page_wiki_topicmodel_start, name='static_parse_page_wiki_topicmodel_start'),
    url(r'^static_parse_page/static_parse_page_wiki_show_topicmodel', views.static_parse_page_wiki_show_topicmodel, name='static_parse_page_wiki_show_topicmodel'),
                       # gecifontos a sorrend matching miatt!

    url(r'^static_parse_page/static_parse_page_index_documents', views.static_parse_page_index_documents, name='static_parse_page_index_documents'),
    url(r'^static_parse_page/static_parse_page_index_refresh_documents', views.static_parse_page_index_refresh_documents, name='static_parse_page_index_refresh_documents'),
    url(r'^static_parse_page/static_parse_page_index_refresh_dictionary', views.static_parse_page_index_refresh_dictionary, name='static_parse_page_index_refresh_dictionary'),
    url(r'^static_parse_page/static_parse_page_index_show_dictionary', views.static_parse_page_index_show_dictionary, name='static_parse_page_index_show_dictionary'),
    url(r'^static_parse_page/static_parse_page_index_topicmodel_start', views.static_parse_page_index_topicmodel_start, name='static_parse_page_index_topicmodel_start'),
    url(r'^static_parse_page/static_parse_page_index_show_topicmodel', views.static_parse_page_index_show_topicmodel, name='static_parse_page_index_show_topicmodel'),



    url(r'dynamic_parse_page$', views.dynamic_parse_page, name='dynamic_parse_page'),
    url(r'dynamic_parse_page/dynamic_parse_page_links_new', views.dynamic_parse_page_links_new, name='dynamic_parse_page_links_new'),
    url(r'dynamic_parse_page/dynamic_parse_page_links_list', views.dynamic_parse_page_links_list, name='dynamic_parse_page_links_list'),
    url(r'dynamic_parse_page/dynamic_parse_page_document_parse', views.dynamic_parse_page_document_parse, name='dynamic_parse_page_document_parse'),
    url(r'dynamic_parse_page/dynamic_parse_page_document_list', views.dynamic_parse_page_document_list, name='dynamic_parse_page_document_list'),

)


# urlpatterns = patterns('',url(r'^$', get_name),)

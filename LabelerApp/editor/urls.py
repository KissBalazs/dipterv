__author__ = 'forestg'
from django.conf.urls import patterns, url, include
# from editor.views import newpost
# from editor.views import get_name
from editor.views import post_new
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
    url(r'^post/multiParse/$', url_multi_parse, name='url_multi_parse'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),


)

# urlpatterns = patterns('',url(r'^$', get_name),)

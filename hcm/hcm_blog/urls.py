from __future__ import unicode_literals
from django.conf.urls import patterns, url
from hcm_blog.views import PostListView, PostDetailView, UserPostListView, PostCreateView, PostUpdateView,\
    PostDeleteView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='blog_post_list'),
    url(r'^/u/(?P<username>\w+)/$', UserPostListView.as_view(), name='blog_user_post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', PostDetailView.as_view(),
        name='blog_post_detail'),

    url(r'^create/$', PostCreateView.as_view(), name='blog_post_create'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/edit/$', PostUpdateView.as_view(),
        name='blog_post_update'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/delete/$', PostDeleteView.as_view(),
        name='blog_post_delete'),
)
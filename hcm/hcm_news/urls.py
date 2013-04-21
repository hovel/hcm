from __future__ import unicode_literals
from django.conf.urls import patterns, url
from hcm_news.views import NewsListView
from hcm_news.views import NewsDetailView

urlpatterns = patterns('',
    url(r'^$', NewsListView.as_view(), name='news_news_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', NewsDetailView.as_view(),
        name='news_news_detail')
)
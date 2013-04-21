from __future__ import unicode_literals
from django.views.generic.dates import DateDetailView
from django.views.generic.list import ListView
from hcm_news.models import News


try:
    from pure_pagination import Paginator
except ImportError:
    # the simplest emulation of django-pure-pagination behavior
    from django.core.paginator import Paginator, Page
    class PageRepr(int):
        def querystring(self):
            return 'page=%s' % self
    Page.pages = lambda self: [PageRepr(i) for i in range(1, self.paginator.num_pages + 1)]


class NewsFitlerMixin(object):
    def get_queryset(self):
        qs = super(NewsFitlerMixin, self).get_queryset()
        return qs.filter(is_published=True)


class NewsListView(NewsFitlerMixin, ListView):
    model = News
    paginate_by = 10
    paginator_class = Paginator


class NewsDetailView(NewsFitlerMixin, DateDetailView):
    model = News
    date_field = 'date_published'
    month_format = '%m'
    day_format = '%d'
    year_format = '%Y'

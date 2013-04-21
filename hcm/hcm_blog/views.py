from django.views.generic.dates import DateDetailView
from django.views.generic.list import ListView
from hcm_blog.models import Post


try:
    from pure_pagination import Paginator
except ImportError:
    # the simplest emulation of django-pure-pagination behavior
    from django.core.paginator import Paginator, Page
    class PageRepr(int):
        def querystring(self):
            return 'page=%s' % self
    Page.pages = lambda self: [PageRepr(i) for i in range(1, self.paginator.num_pages + 1)]


class PostFilterMixin(object):
    def get_queryset(self):
        qs = super(PostFilterMixin, self).get_queryset()
        return qs.filter(is_published=True)


class PostListView(PostFilterMixin, ListView):
    model = Post
    paginate_by = 10
    paginator_class = Paginator


class UserPostListView(PostFilterMixin, ListView):
    model = Post
    paginate_by = 10
    paginator_class = Paginator
    template_name = 'hcm_blog/post_list.html'

    def get_queryset(self):
        qs = super(UserPostListView, self).get_queryset()
        return qs.filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super(UserPostListView, self).get_context_data(**kwargs)
        ctx['username'] = self.kwargs['username']
        return ctx


class PostDetailView(PostFilterMixin, DateDetailView):
    model = Post
    date_field = 'date_published'
    month_format = '%m'
    day_format = '%d'
    year_format = '%Y'
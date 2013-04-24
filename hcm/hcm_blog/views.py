from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.dates import DateDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from hcm_blog.forms import PostCreateUpdateForm, PostCommentForm
from hcm_blog.models import Post, PostComment


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
        if self.request.user.is_authenticated():
            return qs.filter(Q(is_published=True) | Q(author=self.request.user))
        else:
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

    def get_context_data(self, **kwargs):
        ctx = super(PostDetailView, self).get_context_data(**kwargs)
        ctx['comment_form'] = PostCommentForm
        return ctx


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms('hcm_blog.add_post'):
            raise PermissionDenied
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms('hcm_blog.change_post'):
            raise PermissionDenied
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(PostUpdateView, self).get_object(queryset)
        if obj.author == self.request.user or self.request.user.is_staff:
            return obj
        else:
            raise PermissionDenied


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'hcm_blog/post_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms('hcm_blog.delete_post'):
            raise PermissionDenied
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(PostDeleteView, self).get_object(queryset)
        if obj.author == self.request.user or self.request.user.is_staff:
            return obj
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        ctx = super(PostDeleteView, self).get_context_data(**kwargs)
        ctx['action'] = 'delete'
        return ctx

    def get_success_url(self):
        return reverse('blog_post_list')


class PostCommentCreateView(CreateView):
    model = PostComment
    form_class = PostCommentForm
    template_name = 'hcm_blog/post_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.blog_post = get_object_or_404(Post, pk=kwargs['pk'])

        return super(PostCommentCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.post = self.blog_post
        self.object.submit_date = timezone.now()
        self.object.save()
        return super(PostCommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.blog_post.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super(PostCommentCreateView, self).get_context_data(**kwargs)
        ctx['comment_form'] = ctx['form']
        ctx['object'] = self.blog_post
        return ctx
from django.template.base import Library
from hcm_blog.models import Post

register = Library()


@register.assignment_tag
def blog_get_latest(cnt=5):
    return Post.objects.filter(is_published=True).order_by('-date_published')[:cnt]
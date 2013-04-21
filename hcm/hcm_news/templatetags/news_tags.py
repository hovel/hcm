from django.template.base import Library
from hcm_news.models import News

register = Library()


@register.assignment_tag
def news_get_latest(cnt=5):
    return News.objects.filter(is_published=True).order_by('-date_published')[:cnt]
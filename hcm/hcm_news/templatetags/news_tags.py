from django.template.base import Library
from hcm_news.models import News
import markdown

register = Library()


@register.assignment_tag
def news_get_latest(cnt=5):
    return News.objects.filter(is_published=True).order_by('-date_published')[:cnt]


@register.filter
def markdown_str(input_string):
    return markdown.markdown(input_string, safe_mode='remove', html_replacement_text='')
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import markdown
from tagging.fields import TagField


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name=_('author'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(verbose_name=_('blog post body'),
                            help_text=_('Can be used markdown markup for styled output'))
    body_html = models.TextField(verbose_name=_('blog post html'))
    date_published = models.DateField(verbose_name=_('date published'), default=now)
    is_published = models.BooleanField(verbose_name=_('is published'), default=True)
    tags = TagField(verbose_name=_('tags'))

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        unique_together = (('date_published', 'slug'),)
        ordering = ('-date_published', )

    def __str__(self):
        return '%s: %s' % (self.author.username, self.title)

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug,
                                                   'year': self.date_published.strftime('%Y'),
                                                   'month': self.date_published.strftime('%m'),
                                                   'day': self.date_published.strftime('%d')})

    def save(self, *args, **kwargs):
        self.body_html = markdown.markdown(self.body, safe_mode='remove', html_replacement_text='')
        super(Post, self).save(*args, **kwargs)
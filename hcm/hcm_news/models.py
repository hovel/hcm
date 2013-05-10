from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.manager import Manager
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.timezone import now
from sorl.thumbnail.fields import ImageField
from tagging.fields import TagField
from tagging.managers import ModelTaggedItemManager


@python_2_unicode_compatible
class News(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name=_('author'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(verbose_name=_('news body'), help_text=_('Can be used markdown markup for styled output'))
    date_published = models.DateField(verbose_name=_('date published'), default=now)
    is_published = models.BooleanField(verbose_name=_('is published'), default=True)
    image = ImageField(verbose_name=_('image'), upload_to='hcm_news/images/', null=True, blank=True)
    tags = TagField(verbose_name=_('tags'))

    objects = Manager()
    tagged = ModelTaggedItemManager()

    class Meta:
        verbose_name = pgettext_lazy('singular', 'news')
        verbose_name_plural = pgettext_lazy('plural', 'news')
        unique_together = (('date_published', 'slug'),)
        ordering = ('-date_published', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_news_detail', kwargs={'slug': self.slug,
                                                   'year': self.date_published.strftime('%Y'),
                                                   'month': self.date_published.strftime('%m'),
                                                   'day':self.date_published.strftime('%d')})
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.manager import Manager
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import markdown
from tagging.fields import TagField
from tagging.managers import ModelTaggedItemManager
from unidecode import unidecode


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name=_('author'), related_name='blog_posts')
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(verbose_name=_('blog post body'),
                            help_text=_('Can be used markdown markup for styled output'))
    body_html = models.TextField(verbose_name=_('blog post html'))
    date_published = models.DateField(verbose_name=_('date published'), default=now)
    is_published = models.BooleanField(verbose_name=_('is published'), default=True)
    tags = TagField(verbose_name=_('tags'))

    objects = Manager()
    tagged = ModelTaggedItemManager()

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        unique_together = (('date_published', 'slug'),)
        ordering = ('-date_published', )

    def __str__(self):
        return '%s: %s' % (self.author.username, self.title)

    def _url_kwargs(self):
        return {'slug': self.slug, 'year': self.date_published.strftime('%Y'),
                'month': self.date_published.strftime('%m'), 'day': self.date_published.strftime('%d')}

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs=self._url_kwargs())

    def get_update_url(self):
        return reverse('blog_post_update', kwargs=self._url_kwargs())

    def get_delete_url(self):
        return reverse('blog_post_delete', kwargs=self._url_kwargs())

    def save(self, *args, **kwargs):
        self.body_html = markdown.markdown(self.body, safe_mode='remove', html_replacement_text='')
        if not self.slug:
            self.slug = slugify(smart_text(unidecode(self.title)))
        super(Post, self).save(*args, **kwargs)


@python_2_unicode_compatible
class PostComment(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), related_name='blog_post_comments')
    post = models.ForeignKey(Post, verbose_name=_('blog post'), related_name='comments')
    body = models.TextField(verbose_name=_('blog post comment body'))
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    is_removed = models.BooleanField(_('is removed'), default=False)

    class Meta:
        verbose_name = _('blog post comment')
        verbose_name_plural = _('blog post comments')
        ordering = ('-submit_date', )

    def __str__(self):
        return '%s, %s: %s' % (self.post.title[:10], self.user.username, self.body[:20])


def add_blog_permissions(instance, created, **kwargs):
    if created:
        p_add = Permission.objects.get_by_natural_key('add_post', 'hcm_blog', 'post')
        p_change = Permission.objects.get_by_natural_key('change_post', 'hcm_blog', 'post')
        p_delete = Permission.objects.get_by_natural_key('delete_post', 'hcm_blog', 'post')
        instance.user_permissions.add(p_add, p_change, p_delete)


post_save.connect(add_blog_permissions, sender=get_user_model())
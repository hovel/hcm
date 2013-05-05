from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from hcm_news.models import News


class HcmNewsTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin', email='1@2.ru')

    def test_news_detail(self):
        n = News.objects.create(author=self.admin_user, slug='slug')
        response = self.client.get(n.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], n)

    def test_news_list(self):
        n1 = News.objects.create(author=self.admin_user, slug='slug1', is_published=True)
        n2 = News.objects.create(author=self.admin_user, slug='slug2', is_published=False)
        response = self.client.get(reverse('news_news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.context['object_list'][0], n1)
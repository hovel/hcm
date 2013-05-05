from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from tagging.models import Tag
from hcm_blog.models import Post


class HcmBlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user', email='1@1.ru')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin', email='1@2.ru')

    def test_post_detail(self):
        p = Post.objects.create(author=self.admin_user, slug='slug')
        response = self.client.get(p.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], p)

    def test_post_list(self):
        p1 = Post.objects.create(author=self.admin_user, slug='slug1', is_published=True)
        p2 = Post.objects.create(author=self.admin_user, slug='slug2', is_published=False)
        response = self.client.get(reverse('blog_post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)  # only published
        self.assertEqual(response.context['object_list'][0], p1)

        p2.is_published = True
        p2.save()

        p3 = Post.objects.create(author=self.user, slug='slug3', is_published=True)
        response = self.client.get(reverse('blog_user_post_list', kwargs={'username': self.admin_user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 2)  # only admin user posts
        self.assertListEqual(list(response.context['object_list']), [p2, p1])

    def test_post_create_update(self):
        create_url = reverse('blog_post_create')
        # login required
        response = self.client.get(create_url, follow=True)
        self.assertRedirects(response, "%s?next=%s" % (reverse('userena_signin'), create_url))
        response = self.client.post(create_url, follow=True)
        self.assertRedirects(response, "%s?next=%s" % (reverse('userena_signin'), create_url))

        self.client.login(username='admin', password='admin')
        response = self.client.get(create_url, follow=True)
        self.assertEqual(response.status_code, 200)
        data = {
            'title': 'post title',
            'body': '**body**',
            'is_published': True,
            'tags': 'tag1, tag2'
        }
        response = self.client.post(create_url, data=data, follow=True)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)
        p = Post.objects.get(title='post title')
        self.assertEqual(p.author, self.admin_user)
        self.assertIn('<strong>body</strong>', p.body_html)

        update_url = p.get_update_url()
        delete_url = p.get_delete_url()
        self.client.login(username='user', password='user')

        response = self.client.get(update_url, follow=True)
        self.assertEqual(response.status_code, 403)
        response = self.client.post(update_url, follow=True)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(delete_url, follow=True)
        self.assertEqual(response.status_code, 403)
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='admin')
        response = self.client.get(update_url, follow=True)
        self.assertEqual(response.status_code, 200)

        data = {
            'title': 'new title',
            'body': '**new body**',
            'is_published': False,
            'tags': 'tag3, tag4'
        }
        response = self.client.post(update_url, data=data, follow=True)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 4)
        p = Post.objects.get(title='new title')
        self.assertEqual(p.author, self.admin_user)
        self.assertIn('<strong>new body</strong>', p.body_html)

        response = self.client.get(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(delete_url, data=data, follow=True)
        self.assertEqual(Post.objects.count(), 0)



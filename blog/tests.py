from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from hitcount.models import HitCount

from blog.models import Post, Like

"""
testing code for the HopePage
"""


class PrivateHomePageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )

        post = Post.objects.create(
            title="test title",
            owner=user,
        )
        post.liked.set([1])
        HitCount.objects.create(content_object=post)
        self.client.force_login(user)
        self.res = self.client.get(reverse("blog:home-page-main"))

    def test_private_homepage_test(self):
        self.assertEquals(self.res.status_code, 200)

    def test_home_page_count(self):
        num_test = [
            "num_post",
            "num_likes",
            "num_views",
        ]
        for data in num_test:
            self.assertTemplateUsed(self.res, "blog-templates/home/home.html")
            self.assertIn(data, self.res.context,
                          f"key must be equal to {data}")


class PublicHomePageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(reverse("blog:home-page-main"))

    def test_public_home_page(self):
        self.assertNotEquals(self.res.status_code, 200)


class LikePostViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post',
                                        content='This is a test post',
                                        owner=self.user
                                        )
        self.client.login(username='testuser', password='12345')

    def test_like_post_toggle(self):
        self.assertNotIn(self.user, self.post.liked.all())
        response = self.client.post(reverse('blog:like-post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.post.liked.all())
        response = self.client.post(reverse('blog:like-post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.post.liked.all())

    def test_like_post_like_object_created(self):
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())
        response = self.client.post(reverse('blog:like-post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())


class RegisterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post',
                                        content='This is a test post',
                                        owner=self.user
                                        )
        self.client.login(username='testuser', password='12345')

    def test_register_

    def test_register_successful(self):
        self.assertEqual(len(get_user_model().objects.all()), 1)


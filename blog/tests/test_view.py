from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from hitcount.models import HitCount
from blog.models import Post, Like, Comment


"""
testing code for the HopePage
"""


class PrivateHomePageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test", password="12234"
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
            self.assertIn(
                data, self.res.context, f"key must be equal to {data}"
            )


class PublicHomePageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(reverse("blog:home-page-main"))

    def test_public_home_page(self):
        self.assertNotEquals(self.res.status_code, 200)


"""
testing code for the User View
"""


class RegistrationFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("blog:register")

    def test_registration_form_submission(self):
        form_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "tiguti206",
            "password2": "tiguti206",
        }
        self.client.post(self.register_url, form_data)
        self.assertTrue(
            get_user_model().objects.filter(username="test_user").exists()
        )

    def test_empty_registration_form_submission(self):
        response = self.client.post(self.register_url, {}, follow=True)
        self.assertFalse(get_user_model().objects.exists())
        self.assertTemplateUsed(
            response, "blog-templates/accounts/sign-up.html"
        )


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.login(username="test_user", password="test_password")

    def test_user_posts_list_view(self):
        response = self.client.get(reverse("blog:user-posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/accounts/user_posts.html"
        )
        self.assertTrue("post_list" in response.context)
        self.assertTrue("user_id" in response.context)
        self.assertEqual(
            len(response.context["post_list"]), 0
        )  # Assuming user has no posts initially

    def test_user_password_reset_view(self):
        response = self.client.get(reverse("blog:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/accounts/password_reset.html"
        )

    def test_user_password_change_view(self):
        response = self.client.get(reverse("blog:password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/accounts/password_change.html"
        )

    def test_user_login_view(self):
        response = self.client.get(reverse("blog:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/accounts/sign-in.html"
        )


class UserProfileUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            email="test@example.com",
        )
        self.client.login(username="test_user", password="test_password")
        self.update_url = reverse(
            "blog:user-profile", kwargs={"pk": self.user.pk}
        )

    def test_user_profile_update_view(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/accounts/user_profile.html"
        )
        self.assertTrue("user_profile" in response.context)

        for field in [
            "first_name",
            "last_name",
            "email",
            "gender",
            "phone",
            "avatar",
            "birthday",
        ]:
            self.assertContains(response, field)


"""
testing code for the Posts views
"""


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_login(self.user)
        for i in range(10):
            Post.objects.create(
                title=f"Test Post {i}",
                content=f"Test Content {i}",
                owner=self.user,
            )

    def test_post_list_view(self):
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "blog-templates/posts/posts_list.html"
        )
        self.assertTrue("post_list" in response.context)
        self.assertEqual(len(response.context["post_list"]), 5)


class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.login(username="test_user", password="test_password")
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", owner=self.user
        )

    def test_post_delete_view(self):
        response = self.client.post(
            reverse("blog:post-delete", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", owner=self.user
        )
        self.comment_content = "Test comment content"
        self.client.login(username="test_user", password="test_password")

    def test_post_detail_view_post_method(self):
        initial_comment_count = Comment.objects.count()
        response = self.client.post(
            reverse("blog:post-detail", kwargs={"pk": self.post.pk}),
            data={"content": self.comment_content},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), initial_comment_count + 1)


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.login(username="test_user", password="test_password")
        self.post_data = {"title": "Test Post", "content": "Test Content"}

    def test_post_create_view(self):
        response = self.client.post(
            reverse("blog:post-create"), data=self.post_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(
                title="Test Post", content="Test Content"
            ).exists()
        )

    def test_post_create_view_invalid_data(self):
        post_data_invalid = {"title": "", "content": ""}
        response = self.client.post(
            reverse("blog:post-create"), data=post_data_invalid
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="", content="").exists())


"""
testing code for the Likes view
"""


class LikePostViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="12345"
        )
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", owner=self.user
        )
        self.client.login(username="test_user", password="12345")

    def test_like_post_toggle(self):
        self.assertNotIn(self.user, self.post.liked.all())
        response = self.client.post(
            reverse("blog:like-post"), {"post_id": self.post.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.post.liked.all())
        response = self.client.post(
            reverse("blog:like-post"), {"post_id": self.post.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.post.liked.all())

    def test_like_post_like_object_created(self):
        self.assertFalse(
            Like.objects.filter(user=self.user, post=self.post).exists()
        )
        response = self.client.post(
            reverse("blog:like-post"), {"post_id": self.post.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Like.objects.filter(user=self.user, post=self.post).exists()
        )


"""
testing code for the Search view
"""


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.client.force_login(self.user)
        self.post1 = Post.objects.create(
            title="Test Post 1", content="Test Content 1", owner=self.user
        )
        self.post2 = Post.objects.create(
            title="Test Post 2", content="Test Content 2", owner=self.user
        )

    def test_search_view_with_matching_title(self):
        response = self.client.get(
            reverse("blog:search_blog"), {"title_contains": "Test Post 1"}
        )
        self.assertEqual(response.status_code, 200)
        search_results = response.context["search_title"]
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, self.post1.title)

    def test_search_view_with_non_matching_title(self):
        response = self.client.get(
            reverse("blog:search_blog"),
            {"title_contains": "Non-existent Post"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["search_title"], [])

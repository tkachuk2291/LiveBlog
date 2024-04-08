from django.test import TestCase
from datetime import datetime

from blog.forms import User
from blog.models import Post, Like, Comment


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user", email="test@example.com"
        )

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "test_user")

    def test_user_has_username(self):
        self.assertEqual(self.user.username, "test_user")

    def test_user_has_email(self):
        self.assertEqual(self.user.email, "test@example.com")

    def test_user_has_default_avatar(self):
        self.assertEqual(
            self.user.get_avatar,
            "/media/users_photos/default_user_logged_in.png",
        )

    def test_user_has_blank_birthday(self):
        self.assertIsNone(self.user.birthday)

    def test_user_has_blank_phone(self):
        self.assertIsNone(self.user.phone)

    def test_user_format_birthday(self):
        self.user.format_birthday = "01/January/1990"
        self.assertEqual(self.user.birthday, datetime(1990, 1, 1))


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.post = Post.objects.create(
            title="Test Post", owner=self.user, content="Test Content"
        )

    def test_post_num_likes(self):
        self.assertEqual(self.post.num_likes, 0)

    def test_post_has_title(self):
        self.assertEqual(self.post.title, "Test Post")

    def test_post_has_owner(self):
        self.assertEqual(self.post.owner, self.user)

    def test_post_has_content(self):
        self.assertEqual(self.post.content, "Test Content")

    def test_post_has_default_picture(self):
        self.assertEqual(
            self.post.picture, "users_photos_posts/post_default_images.jpeg"
        )


class LikeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.post = Post.objects.create(
            title="Test Post", owner=self.user, content="Test Content"
        )
        self.like = Like.objects.create(
            user=self.user, post=self.post, value="Like"
        )

    def test_like_has_user(self):
        self.assertEqual(self.like.user, self.user)

    def test_like_has_post(self):
        self.assertEqual(self.like.post, self.post)

    def test_like_has_value(self):
        self.assertEqual(self.like.value, "Like")


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.post = Post.objects.create(
            title="Test Post", owner=self.user, content="Test Content"
        )
        self.comment = Comment.objects.create(
            user=self.user, post=self.post, content="Test Comment"
        )

    def test_comment_has_user(self):
        self.assertEqual(self.comment.user, self.user)

    def test_comment_has_post(self):
        self.assertEqual(self.comment.post, self.post)

    def test_comment_has_content(self):
        self.assertEqual(self.comment.content, "Test Comment")

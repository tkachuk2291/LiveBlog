from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_posts")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User , related_name="liked_posts")
    tags = TaggableManager()


LIKE_CHOICE = (
    ("Like", "♥︎"),
    ("Dislike", "♡")
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")
    value = models.CharField(choices=LIKE_CHOICE, max_length=10, default="♡")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name="post_comment")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

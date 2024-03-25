from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _
from django.templatetags.static import static


class User(AbstractUser):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('static/img/illustrations/pp.jpg')


class Post(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_posts")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked_posts")
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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

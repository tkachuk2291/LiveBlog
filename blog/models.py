from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _
from django.templatetags.static import static
from autoslug import AutoSlugField


class User(AbstractUser):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(default="11.jpg", null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.username and not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('static/img/illustrations/pp.jpg')

    @property
    def format_birthday(self):
        return self.birthday


class Post(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_posts")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked", default=None, blank=True)
    slug = AutoSlugField(populate_from="title")
    picture = models.ImageField(default="post_default_images.jpeg", null=True, blank=True)
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICE = (
    ("Dislike", "️🤍"),
    ("Like", "❤️")
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICE, max_length=10, default="♡")

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    content = models.TextField()
    created_time_comment = models.DateTimeField(auto_now_add=True)

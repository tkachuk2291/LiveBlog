from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.templatetags.static import static
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from hitcount.models import HitCount


class User(AbstractUser):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_GENDERLESS = 0
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_GENDERLESS, _("Genderless"))
    ]
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="users_photos/", default="users_photos/default_user_logged_in.png",
                               null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.username and not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/photos_accounts/default_user_logged_in.png')

    @property
    def format_birthday(self):
        if self.birthday:
            return self.birthday.strftime("%d/%B/%Y")
        return ""

    @format_birthday.setter
    def format_birthday(self, value):
        if value:
            self.birthday = datetime.strptime(value, "%d/%B/%Y")
            self.save()


class Post(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_posts")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked", default=None, blank=True)
    slug = AutoSlugField(populate_from="title")
    picture = models.ImageField(upload_to="users_photos_posts", default="users_photos_posts/post_default_images.jpeg",
                                null=True, blank=True)
    tags = TaggableManager()
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

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

from django.contrib import admin

from blog.models import User, Post

admin.site.register(User)
admin.site.register(Post)
# Register your models here.
